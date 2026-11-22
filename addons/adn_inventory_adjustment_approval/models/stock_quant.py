from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class StockQuant(models.Model):
    _inherit = "stock.quant"
    _check_company_auto = True

    adn_adjustment_reason = fields.Char(string="Adjustment Reason", copy=False)
    adn_adjustment_evidence_ids = fields.Many2many(
        "ir.attachment", "adn_inventory_quant_evidence_rel", "quant_id", "attachment_id",
        string="Count Evidence", copy=False, check_company=True,
    )
    adn_inventory_adjustment_request_id = fields.Many2one(
        "adn.inventory.adjustment.request", string="Approval Request", readonly=True,
        copy=False, index=True, ondelete="restrict", check_company=True,
    )
    adn_inventory_adjustment_state = fields.Selection(
        related="adn_inventory_adjustment_request_id.state", readonly=True, store=True,
    )
    adn_inventory_approval_state = fields.Selection(
        related="adn_inventory_adjustment_request_id.approval_state", readonly=True, store=True,
    )

    @api.model
    def _get_inventory_fields_create(self):
        return super()._get_inventory_fields_create()

    @api.model
    def _get_inventory_fields_write(self):
        return super()._get_inventory_fields_write() + [
            "adn_adjustment_reason", "adn_adjustment_evidence_ids",
        ]

    def _adn_check_request_company(self, request):
        if request.company_id not in self.env.companies:
            raise AccessError(_("You cannot modify an inventory adjustment request outside your allowed companies."))
        request_quants = request.quant_ids
        if any(quant.company_id and quant.company_id != request.company_id for quant in request_quants):
            raise AccessError(_("The inventory adjustment request contains a stock quant from another company."))
        if any(not quant.company_id for quant in request_quants) and self.env.company != request.company_id:
            raise AccessError(_("Shared stock quants must be processed in the request company."))

    def _adn_supersede_linked_requests(self, changed_fields):
        requests = self.sudo().mapped("adn_inventory_adjustment_request_id")
        for request in requests:
            if not request or request.state != "submitted":
                continue
            self._adn_check_request_company(request)
            if not request.company_id.adn_inventory_adjustment_approval_enabled:
                raise UserError(_(
                    "This inventory adjustment request is already submitted. Re-enable the approval "
                    "control or complete the existing request before changing its count lines."
                ))
            request._adn_mark_superseded(
                {
                    "invalidated_by_quant_write": True,
                    "request_id": request.id,
                    "quant_ids": sorted(self.ids),
                    "changed_fields": sorted(changed_fields),
                },
                _("An inventory count, reason, or valuation input was changed; a new approval is required."),
            )

    def write(self, vals):
        if "adn_inventory_adjustment_request_id" in vals and not self.env.su:
            raise AccessError(_("Inventory approval links are maintained by the workflow."))
        approval_inputs = {
            "product_id", "location_id", "lot_id", "package_id", "owner_id", "user_id",
            "inventory_quantity", "inventory_quantity_auto_apply", "inventory_quantity_set",
            "accounting_date", "adn_adjustment_reason", "adn_adjustment_evidence_ids",
        }
        if (
            not self.env.su
            and not self.env.context.get("adn_inventory_approval_release")
            and approval_inputs.intersection(vals)
        ):
            self._adn_supersede_linked_requests(approval_inputs.intersection(vals))
        return super().write(vals)

    def action_clear_inventory_quantity(self):
        if not self.env.context.get("adn_inventory_approval_release"):
            self._adn_supersede_linked_requests({"inventory_quantity", "inventory_quantity_set"})
        return super().action_clear_inventory_quantity()

    def action_set_inventory_quantity_zero(self):
        if self.env.context.get("inventory_report_mode") and any(
            (quant.company_id or self.env.company).adn_inventory_adjustment_approval_enabled
            for quant in self
        ):
            self.inventory_quantity = 0
            return self.action_apply_inventory()
        return super().action_set_inventory_quantity_zero()

    @api.model
    def _adn_inventory_valuation_lines(self, quants, company):
        """Estimate each count line using Odoo's current valuation cost logic.

        FIFO decreases use the same cumulative per-product quantity context as
        stock_account when it values outgoing stock moves. Other movements use
        company-specific standard or lot cost as Odoo's inventory fallback.
        """
        quants = quants.exists().sorted("id")
        quants.invalidate_recordset(["adn_adjustment_reason", "adn_adjustment_evidence_ids"])
        has_fifo_out = False
        for quant in quants:
            company_quant = quant.with_company(company).with_context(allowed_company_ids=company.ids)
            difference = company_quant.inventory_quantity - company_quant.quantity
            product = company_quant.product_id.with_company(company).with_context(
                allowed_company_ids=company.ids,
            )
            requires_lot = product.tracking != "none" or (difference > 0 and product.lot_valuated)
            if difference and requires_lot and not company_quant.lot_id:
                raise ValidationError(_(
                    "A lot/serial number is required for inventory adjustments of %(product)s.",
                    product=product.display_name,
                ))
            valued_owner = not company_quant.owner_id or company_quant.owner_id == company.partner_id
            if (
                difference < 0
                and company_quant.cost_method == "fifo"
                and company_quant.location_id._should_be_valued()
                and valued_owner
                and not product.lot_valuated
            ):
                has_fifo_out = True

        if has_fifo_out:
            self.env["stock.move"].invalidate_model(["value", "remaining_qty", "remaining_value"])

        fifo_qty_processed = defaultdict(float)
        result = []
        for quant in quants:
            company_quant = quant.with_company(company).with_context(allowed_company_ids=company.ids)
            product = company_quant.product_id.with_company(company).with_context(
                allowed_company_ids=company.ids,
            )
            difference = company_quant.inventory_quantity - company_quant.quantity
            valued_owner = not company_quant.owner_id or company_quant.owner_id == company.partner_id
            is_valued = company_quant.location_id._should_be_valued() and valued_owner
            if not is_valued:
                unit_cost = 0.0
            elif product.lot_valuated and company_quant.lot_id:
                unit_cost = company_quant.lot_id.with_company(company).with_context(
                    allowed_company_ids=company.ids,
                ).standard_price
            elif difference < 0 and company_quant.cost_method == "fifo":
                fifo_quantity = abs(difference)
                processed_quantity = fifo_qty_processed[product.id]
                fifo_value = product.with_context(
                    fifo_qty_already_processed=processed_quantity,
                )._run_fifo(fifo_quantity)
                unit_cost = fifo_value / fifo_quantity if fifo_quantity else 0.0
                fifo_qty_processed[product.id] += fifo_quantity
            else:
                unit_cost = product.standard_price
            signed_value = difference * unit_cost
            result.append({
                "quant_id": quant.id,
                "product_id": product.id,
                "location_id": company_quant.location_id.id,
                "lot_id": company_quant.lot_id.id or False,
                "package_id": company_quant.package_id.id or False,
                "owner_id": company_quant.owner_id.id or False,
                "counted_by_id": company_quant.user_id.id or False,
                "accounting_date": company_quant.accounting_date,
                "adjustment_reason": company_quant.adn_adjustment_reason or False,
                "evidence_attachment_ids": sorted(company_quant.adn_adjustment_evidence_ids.ids),
                "quantity": company_quant.quantity,
                "counted_quantity": company_quant.inventory_quantity,
                "difference_quantity": difference,
                "cost_method": company_quant.cost_method,
                "tracking": product.tracking,
                "lot_valuated": product.lot_valuated,
                "unit_cost": unit_cost,
                "signed_value": signed_value,
            })
        return result

    def _adn_inventory_conflict_action(self, outdated_quants):
        ctx = dict(self.env.context or {})
        ctx["default_quant_ids"] = self.ids
        ctx["default_quant_to_fix_ids"] = outdated_quants.ids
        return {
            "name": _("Conflict in Inventory Adjustment"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "views": [(False, "form")],
            "res_model": "stock.inventory.conflict",
            "target": "new",
            "context": ctx,
        }

    def _adn_group_adjustment_quants(self, quants, company):
        grouping = company.adn_inventory_adjustment_grouping
        required_settings = (
            company.adn_inventory_adjustment_aggregation,
            grouping,
            company.adn_inventory_adjustment_rounding,
            company.adn_inventory_adjustment_valuation_timing,
        )
        if not all(required_settings):
            raise ValidationError(_(
                "DEC-003 configuration is incomplete for company %(company)s. "
                "Apply the approved aggregation, grouping, rounding, and valuation timing "
                "settings before enabling approval.",
                company=company.display_name,
            ))
        grouped = defaultdict(lambda: self.env["stock.quant"])
        for quant in quants:
            warehouse = quant.warehouse_id
            if grouping == "company_warehouse" and not warehouse:
                raise ValidationError(_(
                    "Inventory adjustment line %(line)s does not resolve to a warehouse. "
                    "Assign the internal location to a warehouse before submitting the adjustment.",
                    line=quant.display_name,
                ))
            category = quant.product_id.product_tmpl_id.categ_id
            key = (
                company.id,
                warehouse.id if grouping in ("company_warehouse", "company_warehouse_category") else False,
                category.id if grouping in ("company_category", "company_warehouse_category") else False,
                quant.accounting_date,
            )
            grouped[key] |= quant
        return grouped

    def _adn_create_adjustment_requests(self, quants, company, inventory_date=None):
        if not self.env.user.has_group(
            "adn_inventory_adjustment_approval.group_inventory_adjustment_requester"
        ):
            raise AccessError(_("You are not authorized to submit inventory adjustments for approval."))
        locked_quants = quants.try_lock_for_update(allow_referencing=True)
        if set(locked_quants.ids) != set(quants.ids):
            raise AccessError(_(
                "Some inventory count lines are being processed by another transaction. "
                "Retry the submission."
            ))
        quants.invalidate_recordset([
            "quantity", "inventory_quantity", "inventory_quantity_set", "is_outdated",
            "adn_inventory_adjustment_request_id", "adn_adjustment_reason", "adn_adjustment_evidence_ids",
        ])
        if quants.filtered("is_outdated"):
            raise ValidationError(_("The stock changed after the count. Refresh and recount before submitting."))
        self._adn_refresh_existing_requests(quants)
        quants = quants.filtered(
            lambda quant: quant.inventory_quantity_set
            and not quant.product_uom_id.is_zero(quant.inventory_quantity - quant.quantity)
        )
        if not quants:
            return self.env["adn.inventory.adjustment.request"]
        grouped = self._adn_group_adjustment_quants(quants, company)
        created_requests = self.env["adn.inventory.adjustment.request"]
        for (_company_id, warehouse_id, category_id, accounting_date), group_quants in grouped.items():
            context_reason = self.env.context.get("inventory_name")
            if isinstance(context_reason, str) and context_reason.strip().casefold() == "physical inventory":
                context_reason = False
            reasons = [
                reason.strip()
                for reason in group_quants.mapped("adn_adjustment_reason")
                if reason and reason.strip()
            ]
            if not context_reason and len(reasons) != len(group_quants):
                raise ValidationError(_(
                    "Enter an ADN Adjustment Reason on every changed inventory count line "
                    "or provide a specific reason in the inventory adjustment dialog."
                ))
            reason_parts = []
            if isinstance(context_reason, str) and context_reason.strip():
                reason_parts.append(context_reason.strip())
            reason_parts.extend(reason for reason in reasons if reason not in reason_parts)
            reason = "\n".join(reason_parts)
            if not reason:
                raise ValidationError(_(
                    "Enter an adjustment reason in the standard Inventory Reason field or in the "
                    "ADN Adjustment Reason field before applying the count."
                ))
            line_values = self._adn_inventory_valuation_lines(group_quants, company)
            currency = company.currency_id
            amount, signed_net = self.env["adn.inventory.adjustment.request"]._adn_aggregate_values(
                line_values,
                company.adn_inventory_adjustment_aggregation,
                currency,
                company.adn_inventory_adjustment_rounding,
            )
            warehouse = self.env["stock.warehouse"].browse(warehouse_id).exists()
            category = self.env["product.category"].browse(category_id).exists()
            request = self.env["adn.inventory.adjustment.request"].sudo().create({
                "company_id": company.id,
                "warehouse_id": warehouse.id or False,
                "category_id": category.id or False,
                "accounting_date": accounting_date or False,
                "inventory_move_date": fields.Datetime.to_datetime(inventory_date) if inventory_date else False,
                "currency_id": currency.id,
                "aggregation_mode": company.adn_inventory_adjustment_aggregation,
                "grouping_mode": company.adn_inventory_adjustment_grouping,
                "rounding_mode": company.adn_inventory_adjustment_rounding,
                "valuation_timing": company.adn_inventory_adjustment_valuation_timing,
                "amount_basis": amount,
                "signed_net_amount": signed_net,
                "reason": reason,
                "requester_id": self.env.user.id,
                "quant_ids": [fields.Command.set(group_quants.ids)],
                "source_evidence_attachment_ids": [
                    fields.Command.set(group_quants.mapped("adn_adjustment_evidence_ids").ids)
                ],
            })
            copied_attachments = self.env["ir.attachment"].sudo()
            for attachment in group_quants.mapped("adn_adjustment_evidence_ids").sudo():
                copied_attachments |= attachment.copy({
                    "res_model": request._name,
                    "res_id": request.id,
                    "company_id": company.id,
                    "datas": attachment.datas,
                })
            if copied_attachments:
                request.write({
                    "evidence_attachment_ids": [fields.Command.set(copied_attachments.ids)],
                })
            request = request.with_env(self.env)
            request._adn_submit_approval()
            created_requests |= request
        return created_requests

    def _adn_refresh_existing_requests(self, quants):
        requests = quants.sudo().mapped("adn_inventory_adjustment_request_id")
        for request in requests:
            if not request or request.state != "submitted":
                continue
            self._adn_check_request_company(request)
            if request.approval_state not in ("pending", "approved"):
                request._adn_mark_superseded(
                    {
                        "invalidated_request_id": request.id,
                        "quant_ids": sorted(request.quant_ids.ids),
                        "approval_state": request.approval_state or False,
                    },
                    _("The previous approval was rejected or cancelled; a new request is required."),
                )
                continue
            try:
                _lines, _amount, _net, snapshot, _approval_amount, _policy_currency = request._adn_current_valuation()
            except (UserError, ValidationError):
                snapshot = {
                    "invalidated_request_id": request.id,
                    "quant_ids": sorted(quants.ids),
                    "changed_fields": ["count_or_policy_state"],
                }
            fingerprint = self.env["adn.approval.request"]._fingerprint(snapshot)
            if fingerprint != request.source_fingerprint:
                request._adn_mark_superseded(
                    snapshot,
                    _("Inventory count, reason, or valuation changed; a new approval is required."),
                )
            else:
                raise UserError(_(
                    "Inventory adjustment %(request)s is already awaiting approval or has been approved. "
                    "Open the request to review its status.",
                    request=request.name,
                ))

    def action_apply_inventory(self, date=None):
        if self.env.context.get("adn_inventory_approval_release"):
            if not self.env.user.has_group(
                "adn_inventory_adjustment_approval.group_inventory_adjustment_executor"
            ):
                raise AccessError(_(
                    "Only an authorized Inventory Adjustment Executor may release an approved adjustment."
                ))
            request = self.env["adn.inventory.adjustment.request"].browse(
                self.env.context.get("adn_inventory_approval_request_id")
            ).exists()
            if request:
                request.invalidate_recordset(["state", "approval_state", "release_in_progress", "quant_ids"])
            if (
                not request
                or request.state != "submitted"
                or request.approval_state != "approved"
                or not request.release_in_progress
            ):
                raise AccessError(_("Only a currently approved inventory adjustment can be released."))
            if set(self.ids) != set(request.quant_ids.ids):
                raise AccessError(_("The selected stock quants do not match the approved adjustment request."))
            try:
                request._adn_assert_release_context(self)
            except (UserError, ValidationError) as error:
                try:
                    (
                        _lines, _amount, _net, current_snapshot,
                        _approval_amount, _policy_currency,
                    ) = request._adn_current_valuation()
                except (UserError, ValidationError):
                    current_snapshot = {
                        "invalidated_request_id": request.id,
                        "quant_ids": sorted(request.quant_ids.ids),
                    }
                request._adn_mark_superseded(
                    current_snapshot,
                    _("Inventory count or valuation changed after approval; a new approval is required."),
                )
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "type": "warning",
                        "title": _("Approval Superseded"),
                        "message": str(error),
                        "sticky": True,
                    },
                }
            return super().action_apply_inventory(date=date)

        outdated = self.filtered("is_outdated")
        if outdated:
            return self._adn_inventory_conflict_action(outdated)

        enabled_quants = self.filtered(
            lambda quant: (quant.company_id or self.env.company).adn_inventory_adjustment_approval_enabled
        )
        if not enabled_quants:
            return super().action_apply_inventory(date=date)

        standard_quants = self - enabled_quants
        approval_quants = enabled_quants.filtered(
            lambda quant: not quant.product_uom_id.is_zero(quant.inventory_quantity - quant.quantity)
        )
        if approval_quants.filtered(lambda quant: not quant.inventory_quantity_set):
            raise UserError(_("Set the counted quantity before submitting the inventory adjustment for approval."))
        unchanged_enabled = enabled_quants - approval_quants
        to_clear = unchanged_enabled.filtered("inventory_quantity_set")

        result = None
        if standard_quants:
            result = super(StockQuant, standard_quants).action_apply_inventory(date=date)
            if result:
                return result
        if to_clear:
            to_clear.action_clear_inventory_quantity()
        if approval_quants:
            requests = self.env["adn.inventory.adjustment.request"]
            for company, company_quants in approval_quants.grouped("company_id").items():
                requests |= self._adn_create_adjustment_requests(
                    company_quants, company or self.env.company, inventory_date=date,
                )
            if requests:
                return {
                    "type": "ir.actions.act_window",
                    "name": _("Inventory Adjustment Approval Requests"),
                    "res_model": "adn.inventory.adjustment.request",
                    "view_mode": "list,form",
                    "domain": [("id", "in", requests.ids)],
                    "target": "current",
                }
        return result

    def _apply_inventory(self, date=None):
        release = self.env.context.get("adn_inventory_approval_release")
        if release:
            if not self.env.user.has_group("adn_inventory_adjustment_approval.group_inventory_adjustment_executor"):
                raise AccessError(_("Only an Inventory Manager may apply an approved inventory adjustment."))
            request = self.env["adn.inventory.adjustment.request"].browse(
                self.env.context.get("adn_inventory_approval_request_id")
            ).exists()
            if request:
                request.invalidate_recordset(["state", "approval_state", "release_in_progress", "quant_ids"])
            if (
                not request
                or request.state != "submitted"
                or request.approval_state != "approved"
                or not request.release_in_progress
                or set(self.ids) != set(request.quant_ids.ids)
            ):
                raise AccessError(_("The inventory adjustment release context is invalid."))
            request._adn_assert_release_context(self)
        else:
            controlled = self.filtered(
                lambda quant: not quant.product_uom_id.is_zero(quant.inventory_quantity - quant.quantity)
                and (
                    (quant.company_id or self.env.company).adn_inventory_adjustment_approval_enabled
                    or (
                        quant.adn_inventory_adjustment_request_id
                        and quant.adn_inventory_adjustment_request_id.state != "released"
                    )
                )
            )
            if controlled:
                raise UserError(_(
                    "This inventory adjustment must pass through the ADN approval workflow. "
                    "Use the standard Apply action to submit it for approval."
                ))
        return super()._apply_inventory(date=date)

    def _get_inventory_move_values(self, qty, location_id, location_dest_id, package_id=False, package_dest_id=False):
        values = super()._get_inventory_move_values(
            qty, location_id, location_dest_id, package_id=package_id, package_dest_id=package_dest_id,
        )
        request_id = self.env.context.get("adn_inventory_approval_request_id")
        if request_id:
            values["adn_inventory_adjustment_request_id"] = request_id
        return values
