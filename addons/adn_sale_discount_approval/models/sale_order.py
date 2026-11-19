from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_DOWN

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


POLICY_CODE = "SO_DISCOUNT_APPROVAL"
CONTROLLED_LINE_THRESHOLD = 5.0
APPROVAL_RELEVANT_ORDER_FIELDS = {
    "partner_id", "pricelist_id", "company_id", "currency_id", "fiscal_position_id",
    "payment_term_id", "order_line",
}
APPROVAL_RELEVANT_LINE_FIELDS = {
    "product_id", "product_uom_qty", "product_uom_id", "price_unit", "discount",
    "name", "display_type", "adn_discount_reason",
}


class SaleOrder(models.Model):
    _inherit = "sale.order"

    adn_discount_approval_request_id = fields.Many2one(
        "adn.approval.request", string="Discount Approval Request", copy=False,
        readonly=True, ondelete="restrict", check_company=True,
    )
    adn_discount_approval_state = fields.Selection([
        ("not_required", "Not Required"), ("not_submitted", "Not Submitted"),
        ("pending", "Pending Approval"), ("approved", "Approved"),
        ("rejected", "Rejected"), ("superseded", "Re-approval Required"),
        ("cancelled", "Approval Cancelled"),
    ], string="Discount Approval Status", compute="_compute_adn_discount_approval_state", store=True)
    adn_discount_approval_fingerprint = fields.Char(
        related="adn_discount_approval_request_id.source_fingerprint", readonly=True, store=True,
    )
    adn_discount_reference_date = fields.Date(
        string="Discount Reference Date", readonly=True, copy=False,
        help="Frozen evaluation date for reference-price currency conversion.",
    )

    @api.depends("adn_discount_approval_request_id", "adn_discount_approval_request_id.state")
    def _compute_adn_discount_approval_state(self):
        for order in self:
            order.adn_discount_approval_state = (
                order.adn_discount_approval_request_id.state
                if order.adn_discount_approval_request_id else "not_submitted"
            )

    def _adn_discount_policy(self, required=False):
        self.ensure_one()
        policy = self.env["adn.approval.policy"].search([
            ("code", "=", POLICY_CODE), ("source_model", "=", "sale.order"),
            ("active", "=", True),
            ("effective_from", "<=", fields.Date.context_today(self)),
            "|", ("effective_to", "=", False), ("effective_to", ">=", fields.Date.context_today(self)),
            "|", ("company_id", "=", self.company_id.id), ("company_id", "=", False),
        ])
        if len(policy) > 1:
            company_policy = policy.filtered(lambda p: p.company_id == self.company_id)
            policy = company_policy or policy.filtered(lambda p: not p.company_id)
        if len(policy) > 1:
            raise ValidationError(_("Multiple active sales discount policies overlap for this company and date."))
        if not policy:
            if required:
                raise ValidationError(_("No active sales discount approval policy is configured. Resolve DEC-002 and activate SO_DISCOUNT_APPROVAL."))
            return self.env["adn.approval.policy"]
        return policy

    def _adn_discount_reference_price(self, line, policy):
        basis = policy.adn_discount_reference_basis
        if basis == "pricelist_unit_price":
            return line.price_unit
        if basis == "product_list_price":
            company_currency = self.company_id.currency_id
            source_price = line.product_id.with_company(self.company_id).lst_price
            if line.product_id.uom_id and line.product_uom_id and line.product_id.uom_id != line.product_uom_id:
                source_price = line.product_id.uom_id._compute_price(source_price, line.product_uom_id)
            if company_currency != self.currency_id:
                source_price = company_currency._convert(
                    source_price, self.currency_id, self.company_id,
                    self.adn_discount_reference_date or (fields.Date.to_date(self.date_order) if self.date_order else fields.Date.context_today(self)),
                )
            return source_price
        if basis == "custom":
            return self._adn_custom_discount_reference_price(line, policy)
        raise ValidationError(_("The sales discount reference price basis is not configured (DEC-002)."))

    def _adn_custom_discount_reference_price(self, line, policy):
        raise ValidationError(_("A custom discount reference price resolver must be implemented before activating this policy."))

    def _adn_discount_effective_unit_price(self, line, policy):
        if policy.adn_discount_cumulative_mode == "single_standard_discount":
            return line.price_unit * (1.0 - (line.discount or 0.0) / 100.0)
        if policy.adn_discount_cumulative_mode == "custom_resolver":
            return self._adn_custom_discount_effective_unit_price(line, policy)
        raise ValidationError(_("The cumulative discount treatment is not configured (DEC-002)."))

    def _adn_custom_discount_effective_unit_price(self, line, policy):
        raise ValidationError(_("A custom cumulative discount resolver must be implemented before activating this policy."))

    def _adn_round_discount(self, percentage, policy):
        digits = int(policy.adn_discount_rounding_digits)
        quantum = Decimal("1").scaleb(-digits)
        rounding = {
            "half_up": ROUND_HALF_UP,
            "half_even": ROUND_HALF_EVEN,
            "down": ROUND_DOWN,
        }.get(policy.adn_discount_rounding_method)
        if rounding is None:
            raise ValidationError(_("Discount rounding method is not configured (DEC-002)."))
        return float(Decimal(str(percentage)).quantize(quantum, rounding=rounding))

    def _adn_line_discount_evaluation(self, line, policy):
        reference = self._adn_discount_reference_price(line, policy)
        effective_unit_price = self._adn_discount_effective_unit_price(line, policy)
        if reference is None or reference <= 0:
            if line.discount or effective_unit_price < (reference or 0.0):
                raise ValidationError(_("A positive discount reference price is required for discounted line '%s'.") % line.display_name)
            return {"reference_price": reference or 0.0, "effective_unit_price": effective_unit_price, "discount_percentage": 0.0}
        raw_percentage = max(0.0, (reference - effective_unit_price) / reference * 100.0)
        percentage = self._adn_round_discount(raw_percentage, policy)
        return {
            "reference_price": reference,
            "effective_unit_price": effective_unit_price,
            "discount_percentage": percentage,
        }

    def _adn_discount_evaluations(self, policy):
        self.ensure_one()
        global_discount_lines = self.order_line.filtered(
            lambda line: not line.display_type and not line.is_downpayment and line._is_global_discount()
        )
        if global_discount_lines and policy.adn_discount_cumulative_mode == "single_standard_discount":
            raise ValidationError(_("This quotation contains a global/cumulative discount. Resolve DEC-002 and configure a custom cumulative discount resolver before approval."))
        evaluations = []
        for line in self.order_line.filtered(lambda l: not l.display_type and not l.is_downpayment and l.product_id and not l._is_global_discount()):
            values = self._adn_line_discount_evaluation(line, policy)
            values["line"] = line
            evaluations.append(values)
        return evaluations

    def _adn_discount_rule_for_percentage(self, policy, percentage):
        rules = policy.rule_ids.filtered("active").sorted(lambda r: (r.sequence, r.id))
        matching = rules.filtered(lambda r: r.matches_discount_percentage(percentage))
        if len(matching) != 1:
            raise ValidationError(_("Expected exactly one discount approval rule for %.6f%%; found %s. Check policy ranges.") % (percentage, len(matching)))
        return matching[0]

    def _adn_discount_snapshot(self, policy, evaluations):
        self.ensure_one()
        lines = []
        for item in evaluations:
            line = item["line"]
            lines.append({
                "line_id": line.id,
                "product_id": line.product_id.id,
                "description": line.name or "",
                "quantity": line.product_uom_qty,
                "uom_id": line.product_uom_id.id,
                "pricelist_unit_price": line.price_unit,
                "odoo_discount_field": line.discount or 0.0,
                "reference_price_basis": policy.adn_discount_reference_basis,
                "reference_price": item["reference_price"],
                "effective_unit_price": item["effective_unit_price"],
                "evaluated_discount_percentage": item["discount_percentage"],
                "reason": line.adn_discount_reason or "",
            })
        return {
            "policy_code": policy.code,
            "policy_version": policy.policy_version,
            "reference_basis": policy.adn_discount_reference_basis,
            "rounding_digits": policy.adn_discount_rounding_digits,
            "rounding_method": policy.adn_discount_rounding_method,
            "cumulative_discount_mode": policy.adn_discount_cumulative_mode,
            "sale_order_id": self.id,
            "sale_order_name": self.name,
            "company_id": self.company_id.id,
            "customer_id": self.partner_id.id,
            "currency_id": self.currency_id.id,
            "pricelist_id": self.pricelist_id.id,
            "amount_untaxed": self.amount_untaxed,
            "lines": lines,
        }

    def _adn_sync_discount_request(self, request):
        self.ensure_one()
        super(SaleOrder, self).write({"adn_discount_approval_request_id": request.id})

    def action_submit_discount_approval(self):
        if not self.env.user.has_group("adn_sale_discount_approval.group_sales_discount_requester"):
            raise AccessError(_("You are not authorized to submit sales discount approvals."))
        for order in self:
            if order.state not in ("draft", "sent"):
                raise UserError(_("Only quotations and draft sales orders can be submitted for discount approval."))
            policy = order._adn_discount_policy(required=True)
            if not order.adn_discount_reference_date:
                order.sudo().write({
                    "adn_discount_reference_date": fields.Date.to_date(order.date_order) if order.date_order else fields.Date.context_today(order),
                })
            evaluations = order._adn_discount_evaluations(policy)
            controlled = [item for item in evaluations if item["discount_percentage"] > CONTROLLED_LINE_THRESHOLD]
            for item in controlled:
                if not item["line"].adn_discount_reason or not item["line"].adn_discount_reason.strip():
                    raise ValidationError(_("A discount reason is mandatory for line '%s' above 5%%.") % item["line"].display_name)
            if not controlled:
                for item in evaluations:
                    item["line"].sudo().write({
                        "adn_discount_reference_price": item["reference_price"],
                        "adn_discount_percentage": item["discount_percentage"],
                        "adn_discount_tier": "WITHIN_SALES_AUTHORITY",
                        "adn_discount_approval_state": "not_required",
                        "adn_discount_approval_item_id": False,
                    })
                continue
            highest = max(item["discount_percentage"] for item in controlled)
            rule = order._adn_discount_rule_for_percentage(policy, highest)
            snapshot = order._adn_discount_snapshot(policy, evaluations)
            current = order.adn_discount_approval_request_id
            if current and current.state in ("pending", "approved"):
                fingerprint = order.env["adn.approval.request"]._fingerprint(snapshot)
                if current.source_fingerprint == fingerprint:
                    raise UserError(_("This sales order already has a current discount approval request."))
                current.action_supersede(snapshot, _("Sales order pricing changed; previous discount approval superseded."))
            item_values = []
            for item in controlled:
                line = item["line"]
                item_values.append({
                    "source_line_model": "sale.order.line",
                    "source_line_res_id": line.id,
                    "item_reference": line.display_name,
                    "basis_value": line.price_subtotal,
                    "basis_percentage": item["discount_percentage"],
                    "tier_code": self._adn_discount_rule_for_percentage(policy, item["discount_percentage"]).tier_code,
                    "state": "pending",
                    "snapshot": {
                        "line_id": line.id,
                        "product_id": line.product_id.id,
                        "reference_price": item["reference_price"],
                        "effective_unit_price": item["effective_unit_price"],
                        "discount_percentage": item["discount_percentage"],
                        "reason": line.adn_discount_reason,
                    },
                })
            request = order.env["adn.approval.request"]._submit_with_rule(
                POLICY_CODE, order, order.amount_untaxed, snapshot,
                reason=_("Sales discount approval for %s") % (order.name or order.display_name),
                item_values=item_values, rule_override_id=rule.id,
                request_currency_id=order.currency_id.id,
            )
            order._adn_sync_discount_request(request)
            for item in evaluations:
                line = item["line"]
                controlled_item = next((v for v in item_values if v["source_line_res_id"] == line.id), None)
                approval_item = request.item_ids.filtered(lambda rec: rec.source_line_res_id == line.id)[:1]
                line.sudo().write({
                    "adn_discount_reference_price": item["reference_price"],
                    "adn_discount_percentage": item["discount_percentage"],
                    "adn_discount_tier": self._adn_discount_rule_for_percentage(policy, item["discount_percentage"]).tier_code if item["discount_percentage"] > CONTROLLED_LINE_THRESHOLD else "WITHIN_SALES_AUTHORITY",
                    "adn_discount_approval_state": "pending" if controlled_item else "not_required",
                    "adn_discount_approval_item_id": approval_item.id if approval_item else False,
                })
            order.message_post(body=_("Submitted discount approval %s. Highest controlled line discount: %.4f%% (%s).") % (request.name, highest, rule.tier_code))
        return True

    def _adn_current_discount_snapshot(self, request):
        self.ensure_one()
        policy = request.policy_id
        evaluations = self._adn_discount_evaluations(policy)
        return self._adn_discount_snapshot(policy, evaluations), evaluations

    def _adn_handle_discount_amendment(self):
        for order in self.exists():
            request = order.adn_discount_approval_request_id
            if not request or request.state not in ("pending", "approved"):
                continue
            snapshot, evaluations = order._adn_current_discount_snapshot(request)
            fingerprint = order.env["adn.approval.request"]._fingerprint(snapshot)
            if fingerprint == request.source_fingerprint:
                continue
            request.action_supersede(snapshot, _("Approval-relevant sales order values changed; re-approval is required."))
            for item in request.item_ids:
                line = order.order_line.filtered(lambda l: l.id == item.source_line_res_id)
                if line:
                    line.sudo().write({"adn_discount_approval_state": "superseded"})
            order.invalidate_recordset(["adn_discount_approval_state", "adn_discount_approval_fingerprint"])
            order.message_post(body=_("The previous discount approval was superseded. Review discount reasons and submit the quotation again."))

    def _adn_assert_discount_approval_released(self):
        for order in self:
            policy = order._adn_discount_policy(required=False)
            if not policy:
                # Fail closed for any explicit discount until DEC-002 is configured.
                discounted = order.order_line.filtered(lambda l: not l.display_type and (l.discount or 0.0) > 0)
                if discounted:
                    raise UserError(_("Discounted sales orders are blocked until the Sales Discount Approval policy and DEC-002 reference basis are configured."))
                continue
            evaluations = order._adn_discount_evaluations(policy)
            controlled = [item for item in evaluations if item["discount_percentage"] > CONTROLLED_LINE_THRESHOLD]
            if not controlled:
                continue
            request = order.adn_discount_approval_request_id
            if not request:
                raise UserError(_("Sales order %s contains a discount above 5%% and must be submitted for approval.") % order.display_name)
            snapshot = order._adn_discount_snapshot(policy, evaluations)
            request.assert_released(order, POLICY_CODE, snapshot)
            if request.state != "approved":
                raise UserError(_("Sales discount approval is not complete."))

    def action_open_discount_approval(self):
        self.ensure_one()
        if not self.adn_discount_approval_request_id:
            raise UserError(_("This sales order has no discount approval request."))
        return {
            "type": "ir.actions.act_window", "name": _("Sales Discount Approval"),
            "res_model": "adn.approval.request", "view_mode": "form",
            "res_id": self.adn_discount_approval_request_id.id, "target": "current",
        }

    def action_confirm(self):
        self._adn_assert_discount_approval_released()
        return super().action_confirm()

    def _action_confirm(self):
        self._adn_assert_discount_approval_released()
        return super()._action_confirm()

    @api.model_create_multi
    def create(self, vals_list):
        protected = {"adn_discount_approval_request_id", "adn_discount_reference_date"}
        if not self.env.su and any(protected.intersection(vals) for vals in vals_list):
            raise AccessError(_("Discount approval linkage and reference date are managed by the server-side workflow."))
        return super().create(vals_list)

    def write(self, vals):
        protected = {"adn_discount_approval_request_id", "adn_discount_reference_date"}
        if protected.intersection(vals) and not self.env.su:
            raise AccessError(_("Discount approval linkage and reference date are managed by the server-side workflow."))
        if vals.get("state") in ("sale", "done"):
            self._adn_assert_discount_approval_released()
        result = super().write(vals)
        if APPROVAL_RELEVANT_ORDER_FIELDS.intersection(vals):
            self._adn_handle_discount_amendment()
        return result


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    adn_discount_reason = fields.Text(string="Discount Exception Reason", copy=False)
    adn_discount_reference_price = fields.Monetary(
        string="Approval Reference Price", currency_field="currency_id", readonly=True, copy=False,
    )
    adn_discount_percentage = fields.Float(string="Evaluated Discount %", digits=(16, 6), readonly=True, copy=False)
    adn_discount_tier = fields.Char(string="Discount Approval Tier", readonly=True, copy=False)
    adn_discount_approval_state = fields.Selection([
        ("not_required", "Not Required"), ("pending", "Pending"),
        ("approved", "Approved"), ("rejected", "Rejected"),
        ("superseded", "Re-approval Required"), ("cancelled", "Cancelled"),
    ], string="Line Approval Status", readonly=True, copy=False)
    adn_discount_approval_item_id = fields.Many2one(
        "adn.approval.item", string="Approval Item", readonly=True, copy=False, ondelete="restrict",
    )

    @api.model_create_multi
    def create(self, vals_list):
        protected = {
            "adn_discount_reference_price", "adn_discount_percentage", "adn_discount_tier",
            "adn_discount_approval_state", "adn_discount_approval_item_id",
        }
        if not self.env.su and any(protected.intersection(vals) for vals in vals_list):
            raise AccessError(_("Discount evaluation snapshots and approval links are managed by the server-side workflow."))
        lines = super().create(vals_list)
        lines.mapped("order_id")._adn_handle_discount_amendment()
        return lines

    def unlink(self):
        orders = self.mapped("order_id")
        result = super().unlink()
        orders._adn_handle_discount_amendment()
        return result

    def write(self, vals):
        protected = {
            "adn_discount_reference_price", "adn_discount_percentage", "adn_discount_tier",
            "adn_discount_approval_state", "adn_discount_approval_item_id",
        }
        if protected.intersection(vals) and not self.env.su:
            raise AccessError(_("Discount evaluation snapshots and approval links are managed by the server-side workflow."))
        orders = self.mapped("order_id")
        result = super().write(vals)
        if APPROVAL_RELEVANT_LINE_FIELDS.intersection(vals):
            orders._adn_handle_discount_amendment()
        return result


class AdnApprovalRequest(models.Model):
    _inherit = "adn.approval.request"

    def action_approve(self, comment=None):
        result = super().action_approve(comment=comment)
        for request in self.filtered(lambda r: r.policy_id.code == POLICY_CODE and r.state == "approved"):
            request.item_ids.sudo().write({"state": "approved"})
            lines = self.env["sale.order.line"].browse(request.item_ids.mapped("source_line_res_id")).exists()
            lines.sudo().write({"adn_discount_approval_state": "approved"})
            order = self.env["sale.order"].browse(request.source_res_id).exists()
            if order:
                order.sudo().message_post(body=_("Sales discount approval %s completed.") % request.name)
        return result

    def action_reject(self, reason):
        result = super().action_reject(reason)
        for request in self.filtered(lambda r: r.policy_id.code == POLICY_CODE and r.state == "rejected"):
            request.item_ids.sudo().write({"state": "rejected"})
            lines = self.env["sale.order.line"].browse(request.item_ids.mapped("source_line_res_id")).exists()
            lines.sudo().write({"adn_discount_approval_state": "rejected"})
            order = self.env["sale.order"].browse(request.source_res_id).exists()
            if order:
                order.sudo().message_post(body=_("Sales discount approval %s rejected: %s") % (request.name, reason))
        return result

    def action_cancel(self, reason=None):
        result = super().action_cancel(reason=reason)
        for request in self.filtered(lambda r: r.policy_id.code == POLICY_CODE and r.state == "cancelled"):
            lines = self.env["sale.order.line"].browse(request.item_ids.mapped("source_line_res_id")).exists()
            lines.sudo().write({"adn_discount_approval_state": "cancelled"})
        return result
