from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


POLICY_CODE = "INVENTORY_ADJUSTMENT_APPROVAL"


class AdnInventoryAdjustmentRequest(models.Model):
    _name = "adn.inventory.adjustment.request"
    _description = "ADN Inventory Adjustment Approval Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "requested_at desc, id desc"
    _check_company_auto = True

    name = fields.Char(required=True, readonly=True, copy=False, default="New", index=True)
    company_id = fields.Many2one("res.company", required=True, readonly=True, index=True)
    warehouse_id = fields.Many2one("stock.warehouse", readonly=True, index=True, check_company=True)
    currency_id = fields.Many2one("res.currency", required=True, readonly=True)
    aggregation_mode = fields.Selection(
        [("sum_absolute", "Sum of Absolute Line Values"), ("absolute_net", "Absolute Net Value")],
        required=True, readonly=True,
    )
    grouping_mode = fields.Selection(
        [
            ("company", "Company"),
            ("company_warehouse", "Company and Warehouse"),
            ("company_category", "Company and Product Category"),
            ("company_warehouse_category", "Company, Warehouse and Product Category"),
        ],
        required=True, readonly=True,
    )
    category_id = fields.Many2one("product.category", readonly=True, index=True)
    accounting_date = fields.Date(readonly=True, index=True)
    inventory_move_date = fields.Datetime(readonly=True)
    rounding_mode = fields.Selection(
        [("aggregate", "Round Final Aggregate"), ("per_line", "Round Each Line")],
        required=True, readonly=True,
    )
    valuation_timing = fields.Selection(
        [("submission_release", "Submission and Release Revalidation")],
        required=True, readonly=True,
    )
    amount_basis = fields.Monetary(currency_field="currency_id", readonly=True, tracking=True)
    signed_net_amount = fields.Monetary(currency_field="currency_id", readonly=True)
    reason = fields.Text(required=True, readonly=True, tracking=True)
    requester_id = fields.Many2one("res.users", required=True, readonly=True, default=lambda self: self.env.user)
    requested_at = fields.Datetime(required=True, readonly=True, default=fields.Datetime.now)
    state = fields.Selection(
        [
            ("submitted", "Submitted"),
            ("released", "Released"),
            ("superseded", "Superseded"),
        ],
        required=True, default="submitted", readonly=True, tracking=True, index=True,
    )
    approval_request_id = fields.Many2one(
        "adn.approval.request", readonly=True, copy=False, ondelete="restrict", index=True, check_company=True,
    )
    approval_state = fields.Selection(related="approval_request_id.state", readonly=True, store=True)
    source_fingerprint = fields.Char(readonly=True, copy=False, index=True)
    quant_ids = fields.Many2many(
        "stock.quant", "adn_inventory_adjustment_quant_rel", "request_id", "quant_id",
        string="Inventory Count Lines", readonly=True, copy=False, check_company=True,
    )
    line_ids = fields.One2many(
        "adn.inventory.adjustment.line", "request_id", string="Adjustment Snapshot Lines", readonly=True,
    )
    evidence_attachment_ids = fields.Many2many(
        "ir.attachment", "adn_inventory_adjustment_attachment_rel", "request_id", "attachment_id",
        string="Count Evidence", readonly=True, copy=False, check_company=True,
    )
    source_evidence_attachment_ids = fields.Many2many(
        "ir.attachment", "adn_inventory_adjustment_source_attachment_rel", "request_id", "attachment_id",
        string="Source Count Evidence", readonly=True, copy=False, check_company=True,
    )
    stock_move_ids = fields.One2many(
        "stock.move", "adn_inventory_adjustment_request_id", string="Generated Stock Moves", readonly=True,
    )
    actual_valuation_amount = fields.Monetary(currency_field="currency_id", readonly=True, copy=False)
    released_at = fields.Datetime(readonly=True, copy=False)
    released_by_id = fields.Many2one("res.users", readonly=True, copy=False)
    release_in_progress = fields.Boolean(readonly=True, copy=False, default=False)
    line_count = fields.Integer(compute="_compute_line_count")

    @api.depends("line_ids")
    def _compute_line_count(self):
        for request in self:
            request.line_count = len(request.line_ids)

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.user.has_group("adn_inventory_adjustment_approval.group_inventory_adjustment_requester"):
            raise AccessError(_("You are not authorized to create inventory adjustment approval requests."))
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code("adn.inventory.adjustment.request") or "New"
        return super().create(vals_list)

    def write(self, vals):
        protected = {
            "name", "company_id", "warehouse_id", "category_id", "accounting_date", "inventory_move_date",
            "currency_id", "aggregation_mode",
            "grouping_mode", "rounding_mode", "valuation_timing", "amount_basis", "signed_net_amount",
            "reason", "requester_id", "requested_at", "state", "evidence_attachment_ids",
            "release_in_progress",
            "source_evidence_attachment_ids",
            "approval_request_id", "source_fingerprint", "quant_ids", "line_ids", "actual_valuation_amount",
            "released_at", "released_by_id",
        }
        if protected.intersection(vals) and not self.env.su:
            raise AccessError(_("Inventory adjustment approval data is maintained by the workflow."))
        return super().write(vals)

    @api.model
    def _adn_aggregate_values(self, line_values, aggregation_mode, currency, rounding_mode):
        values = [line["signed_value"] for line in line_values]
        if rounding_mode == "per_line":
            values = [currency.round(value) for value in values]
        elif rounding_mode != "aggregate":
            raise ValidationError(_("An inventory adjustment rounding mode must be configured."))
        signed_net = sum(values)
        if aggregation_mode == "sum_absolute":
            amount = sum(abs(value) for value in values)
        elif aggregation_mode == "absolute_net":
            amount = abs(signed_net)
        else:
            raise ValidationError(_("An inventory adjustment aggregation mode must be configured."))
        return currency.round(amount), currency.round(signed_net)

    @api.model
    def _currency_amount(self, company, amount, currency):
        company_currency = company.currency_id
        if company_currency == currency:
            return currency.round(amount)
        return company_currency._convert(
            amount, currency, company, fields.Date.context_today(self),
        )

    def _adn_current_valuation(self):
        self.ensure_one()
        self.company_id.invalidate_recordset([
            "adn_inventory_adjustment_aggregation", "adn_inventory_adjustment_grouping",
            "adn_inventory_adjustment_rounding", "adn_inventory_adjustment_valuation_timing",
        ])
        quants = self.quant_ids.exists().sorted("id")
        if not quants:
            raise ValidationError(_("The inventory count lines no longer exist."))
        if any(quant.company_id and quant.company_id != self.company_id for quant in quants):
            raise ValidationError(_("All inventory count lines must belong to the request company."))
        if any(not quant.company_id for quant in quants) and self.env.company != self.company_id:
            raise AccessError(_("Shared stock quants must be processed in the request company."))
        quants.invalidate_recordset([
            "quantity", "inventory_quantity", "inventory_quantity_set", "is_outdated",
            "product_id", "location_id", "lot_id", "package_id", "owner_id", "warehouse_id",
            "accounting_date", "cost_method", "adn_adjustment_reason", "adn_adjustment_evidence_ids",
        ])
        if any(not quant.inventory_quantity_set for quant in quants):
            raise ValidationError(_("One or more count quantities are no longer pending application."))
        quants.mapped("product_id").invalidate_recordset([
            "standard_price", "cost_method", "lot_valuated", "tracking",
        ])
        quants.mapped("lot_id").invalidate_recordset(["standard_price"])

        policy = self.env["adn.approval.policy"].get_active_policy(
            POLICY_CODE, self.company_id, self._name,
        )
        policy.ensure_one()
        policy.invalidate_recordset(["policy_version", "currency_id", "active"])
        if (
            self.company_id.adn_inventory_adjustment_aggregation != self.aggregation_mode
            or self.company_id.adn_inventory_adjustment_grouping != self.grouping_mode
            or self.company_id.adn_inventory_adjustment_rounding != self.rounding_mode
            or self.company_id.adn_inventory_adjustment_valuation_timing != self.valuation_timing
        ):
            raise ValidationError(_("DEC-003 configuration changed after this request was submitted."))
        if self.grouping_mode in ("company_category", "company_warehouse_category"):
            if any(quant.product_id.product_tmpl_id.categ_id != self.category_id for quant in quants):
                raise ValidationError(_("The product category no longer matches the approved request grouping."))
        if self.grouping_mode in ("company_warehouse", "company_warehouse_category"):
            if any(quant.warehouse_id != self.warehouse_id for quant in quants):
                raise ValidationError(_("The warehouse no longer matches the approved request grouping."))
        if any(quant.accounting_date != self.accounting_date for quant in quants):
            raise ValidationError(_("The accounting date no longer matches the approved request grouping."))
        source_evidence_metadata = sorted(
            (attachment.checksum or "", attachment.name or "", attachment.mimetype or "")
            for attachment in self.source_evidence_attachment_ids
        )
        request_evidence_metadata = sorted(
            (attachment.checksum or "", attachment.name or "", attachment.mimetype or "")
            for attachment in self.evidence_attachment_ids
        )
        if source_evidence_metadata != request_evidence_metadata:
            raise ValidationError(_(
                "The inventory adjustment evidence set is missing or has changed; submit a new request."
            ))
        line_values = self.env["stock.quant"]._adn_inventory_valuation_lines(quants, self.company_id)
        amount, signed_net = self._adn_aggregate_values(
            line_values, self.aggregation_mode, self.currency_id, self.rounding_mode,
        )
        policy_currency = policy.currency_id or self.company_id.currency_id
        approval_amount = self._currency_amount(self.company_id, amount, policy_currency)
        snapshot = {
            "policy_code": POLICY_CODE,
            "policy_version": policy.policy_version,
            "company_id": self.company_id.id,
            "warehouse_id": self.warehouse_id.id or False,
            "currency_id": self.currency_id.id,
            "policy_currency_id": policy_currency.id,
            "approval_amount": approval_amount,
            "aggregation_mode": self.aggregation_mode,
            "grouping_mode": self.grouping_mode,
            "category_id": self.category_id.id or False,
            "accounting_date": self.accounting_date.isoformat() if self.accounting_date else False,
            "inventory_move_date": self.inventory_move_date.isoformat() if self.inventory_move_date else False,
            "rounding_mode": self.rounding_mode,
            "valuation_timing": self.valuation_timing,
            "reason": self.reason,
            "evidence_attachment_ids": sorted(self.source_evidence_attachment_ids.ids),
            "evidence_files": source_evidence_metadata,
            "amount_basis": amount,
            "signed_net_amount": signed_net,
            "lines": [
                {
                    "quant_id": line["quant_id"],
                    "product_id": line["product_id"],
                    "location_id": line["location_id"],
                    "lot_id": line["lot_id"],
                    "package_id": line["package_id"],
                    "owner_id": line["owner_id"],
                    "counted_by_id": line["counted_by_id"],
                    "accounting_date": line["accounting_date"].isoformat() if line["accounting_date"] else False,
                    "adjustment_reason": line["adjustment_reason"],
                    "evidence_attachment_ids": line["evidence_attachment_ids"],
                    "quantity": line["quantity"],
                    "counted_quantity": line["counted_quantity"],
                    "difference_quantity": line["difference_quantity"],
                    "cost_method": line["cost_method"],
                    "tracking": line["tracking"],
                    "lot_valuated": line["lot_valuated"],
                    "unit_cost": line["unit_cost"],
                    "signed_value": line["signed_value"],
                }
                for line in line_values
            ],
        }
        return line_values, amount, signed_net, snapshot, approval_amount, policy_currency

    def _adn_submit_approval(self):
        self.ensure_one()
        line_values, amount, signed_net, snapshot, approval_amount, policy_currency = self._adn_current_valuation()
        request = self.env["adn.approval.request"]._submit_with_rule(
            POLICY_CODE,
            self,
            approval_amount,
            snapshot,
            reason=_("Inventory adjustment approval for %s") % self.name,
            request_currency_id=policy_currency.id,
        )
        line_commands = [(0, 0, {
            "quant_id": line["quant_id"],
            "quant_reference": str(line["quant_id"]),
            "product_id": line["product_id"],
            "location_id": line["location_id"],
            "lot_id": line["lot_id"],
            "package_id": line["package_id"],
            "owner_id": line["owner_id"],
            "counted_by_id": line["counted_by_id"],
            "accounting_date": line["accounting_date"],
            "adjustment_reason": line["adjustment_reason"],
            "quantity": line["quantity"],
            "counted_quantity": line["counted_quantity"],
            "difference_quantity": line["difference_quantity"],
            "cost_method": line["cost_method"],
            "tracking": line["tracking"],
            "lot_valuated": line["lot_valuated"],
            "unit_cost": line["unit_cost"],
            "signed_value": line["signed_value"],
        }) for line in line_values]
        self.sudo().write({
            "amount_basis": amount,
            "signed_net_amount": signed_net,
            "approval_request_id": request.id,
            "source_fingerprint": request.source_fingerprint,
            "line_ids": line_commands,
        })
        self.quant_ids.sudo().write({"adn_inventory_adjustment_request_id": self.id})
        self.message_post(body=_("Submitted for approval: %s (%s %s).") % (
            request.name, policy_currency.name, approval_amount,
        ))
        return request

    def _adn_mark_superseded(self, new_snapshot, reason):
        for record in self:
            approval_request = record.approval_request_id
            if approval_request and approval_request.state in ("pending", "approved"):
                record.sudo().approval_request_id.action_supersede(new_snapshot, reason)
            record.sudo().write({"state": "superseded", "release_in_progress": False})
            record.message_post(body=_("Inventory adjustment approval superseded: %s") % reason)
            record.quant_ids.sudo().filtered(
                lambda quant: quant.adn_inventory_adjustment_request_id == record
            ).write({"adn_inventory_adjustment_request_id": False})

    def _adn_assert_release_context(self, quants):
        self.ensure_one()
        if self.state != "submitted" or self.approval_state != "approved":
            raise UserError(_("The inventory adjustment approval is not complete."))
        if set(quants.ids) != set(self.quant_ids.ids):
            raise ValidationError(_("The selected stock quants do not match the approved adjustment request."))
        locked_quants = quants.try_lock_for_update(allow_referencing=True)
        if set(locked_quants.ids) != set(quants.ids):
            raise AccessError(_(
                "Some inventory count lines are being processed by another transaction. "
                "Retry the release."
            ))
        quants.invalidate_recordset([
            "quantity", "inventory_quantity", "inventory_quantity_set", "is_outdated",
        ])
        if quants.filtered("is_outdated"):
            raise ValidationError(_("The stock changed after the count. Refresh and recount before release."))
        _lines, _amount, _net, snapshot, _approval_amount, _policy_currency = self._adn_current_valuation()
        self.approval_request_id.assert_released(self, POLICY_CODE, snapshot)
        if self.source_fingerprint != self.approval_request_id.source_fingerprint:
            raise UserError(_("The approved inventory adjustment fingerprint is stale."))
        return True

    def action_open_approval_request(self):
        self.ensure_one()
        if not self.approval_request_id:
            raise UserError(_("This inventory adjustment has no approval request."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Inventory Adjustment Approval"),
            "res_model": "adn.approval.request",
            "view_mode": "form",
            "res_id": self.approval_request_id.id,
            "target": "current",
        }

    def action_release(self):
        self.ensure_one()
        self.invalidate_recordset(["state", "approval_state", "release_in_progress", "quant_ids"])
        if not self.env.user.has_group("adn_inventory_adjustment_approval.group_inventory_adjustment_executor"):
            raise AccessError(_("Only an Inventory Manager may apply an approved inventory adjustment."))
        if self.state != "submitted" or self.approval_state != "approved":
            raise UserError(_("Only an approved inventory adjustment can be released."))
        release_quants = self.quant_ids.exists().sorted("id").with_company(self.company_id).with_context(
            allowed_company_ids=self.company_id.ids,
            adn_inventory_approval_release=True,
            adn_inventory_approval_request_id=self.id,
            inventory_name=self.reason.replace("\n", " / ")[:250],
        )
        self.sudo().write({"release_in_progress": True})
        self.invalidate_recordset(["release_in_progress"])
        result = release_quants.action_apply_inventory(date=self.inventory_move_date)
        if release_quants.filtered("inventory_quantity_set"):
            self.sudo().write({"release_in_progress": False})
            return result or {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "type": "warning",
                    "title": _("Inventory Adjustment Not Applied"),
                    "message": _("The count remains pending. Refresh the count and retry the release."),
                    "sticky": True,
                },
            }
        self.invalidate_recordset(["stock_move_ids"])
        moves = self.stock_move_ids.exists()
        moves.invalidate_recordset(["value"])
        actual = sum(abs(move.value) for move in moves)
        self.sudo().write({
            "state": "released",
            "release_in_progress": False,
            "actual_valuation_amount": self.currency_id.round(actual),
            "released_at": fields.Datetime.now(),
            "released_by_id": self.env.user.id,
        })
        self.message_post(body=_("Inventory adjustment applied by %s.") % self.env.user.display_name)
        release_quants.sudo().write({
            "adn_adjustment_reason": False,
            "adn_adjustment_evidence_ids": [fields.Command.clear()],
        })
        return result or {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "success",
                "title": _("Inventory Adjustment Applied"),
                "message": _("The approved inventory adjustment has been applied."),
                "sticky": False,
            },
        }


class AdnInventoryAdjustmentLine(models.Model):
    _name = "adn.inventory.adjustment.line"
    _description = "ADN Inventory Adjustment Snapshot Line"
    _order = "id"
    _check_company_auto = True

    request_id = fields.Many2one(
        "adn.inventory.adjustment.request", required=True, readonly=True, ondelete="cascade", index=True,
        check_company=True,
    )
    company_id = fields.Many2one(related="request_id.company_id", store=True, readonly=True, index=True)
    currency_id = fields.Many2one(related="request_id.currency_id", readonly=True)
    quant_id = fields.Many2one(
        "stock.quant", readonly=True, ondelete="set null", index=True, check_company=True,
    )
    quant_reference = fields.Char(required=True, readonly=True)
    product_id = fields.Many2one(
        "product.product", required=True, readonly=True, ondelete="restrict", check_company=True,
    )
    location_id = fields.Many2one(
        "stock.location", required=True, readonly=True, ondelete="restrict", check_company=True,
    )
    lot_id = fields.Many2one("stock.lot", readonly=True, ondelete="restrict", check_company=True)
    package_id = fields.Many2one("stock.package", readonly=True, ondelete="restrict", check_company=True)
    owner_id = fields.Many2one("res.partner", readonly=True, ondelete="restrict")
    counted_by_id = fields.Many2one("res.users", readonly=True)
    accounting_date = fields.Date(readonly=True)
    adjustment_reason = fields.Char(readonly=True)
    quantity = fields.Float(readonly=True, digits="Product Unit")
    counted_quantity = fields.Float(readonly=True, digits="Product Unit")
    difference_quantity = fields.Float(readonly=True, digits="Product Unit")
    cost_method = fields.Selection(
        [("standard", "Standard"), ("average", "AVCO"), ("fifo", "FIFO")], readonly=True,
    )
    tracking = fields.Selection(
        [("none", "No Tracking"), ("lot", "By Lots"), ("serial", "By Unique Serial Number")],
        readonly=True,
    )
    lot_valuated = fields.Boolean(readonly=True)
    unit_cost = fields.Monetary(currency_field="currency_id", readonly=True)
    signed_value = fields.Monetary(currency_field="currency_id", readonly=True)

    def write(self, vals):
        if not self.env.su:
            raise AccessError(_("Inventory adjustment snapshot lines are immutable."))
        return super().write(vals)

    def unlink(self):
        if not self.env.su:
            raise AccessError(_("Inventory adjustment snapshot lines cannot be deleted."))
        return super().unlink()
