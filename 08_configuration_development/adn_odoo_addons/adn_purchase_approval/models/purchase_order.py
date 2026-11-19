from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


POLICY_CODE = "PO_APPROVAL"
APPROVAL_RELEVANT_PO_FIELDS = {"partner_id", "currency_id", "date_order", "company_id", "order_line"}
APPROVAL_RELEVANT_LINE_FIELDS = {
    "product_id", "name", "product_qty", "product_uom", "price_unit",
    "discount", "date_planned", "product_uom_id", "tax_ids",
}


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    adn_approval_request_id = fields.Many2one(
        "adn.approval.request", string="Approval Request", copy=False,
        readonly=True, ondelete="restrict", check_company=True,
    )
    adn_approval_state = fields.Selection([
        ("not_submitted", "Not Submitted"),
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("superseded", "Re-approval Required"),
        ("cancelled", "Approval Cancelled"),
    ], string="ADN Approval Status", compute="_compute_adn_approval_state", store=True, copy=False)
    adn_approval_tier = fields.Char(
        string="Approval Tier", related="adn_approval_request_id.tier_code", store=True, readonly=True,
    )
    adn_approval_amount = fields.Monetary(
        string="Approval Amount (Company Currency)", currency_field="adn_approval_currency_id",
        related="adn_approval_request_id.amount_basis", store=True, readonly=True,
    )
    adn_approval_currency_id = fields.Many2one(
        "res.currency", related="adn_approval_request_id.currency_id", string="Approval Currency", readonly=True,
    )
    adn_approval_fingerprint = fields.Char(
        string="Approval Fingerprint", related="adn_approval_request_id.source_fingerprint", store=True, readonly=True,
    )
    adn_submitted_at = fields.Datetime(
        string="Submitted for Approval At", related="adn_approval_request_id.requested_at", store=True, readonly=True,
    )
    adn_last_approval_at = fields.Datetime(
        string="Last Approved At", compute="_compute_adn_last_approval_at", store=True,
    )

    @api.depends("adn_approval_request_id", "adn_approval_request_id.state")
    def _compute_adn_approval_state(self):
        for order in self:
            order.adn_approval_state = order.adn_approval_request_id.state if order.adn_approval_request_id else "not_submitted"

    @api.depends("adn_approval_request_id", "adn_approval_request_id.state", "adn_approval_request_id.completed_at")
    def _compute_adn_last_approval_at(self):
        for order in self:
            request = order.adn_approval_request_id
            order.adn_last_approval_at = request.completed_at if request and request.state == "approved" else False

    def _adn_approval_policy(self):
        self.ensure_one()
        return self.env["adn.approval.policy"].get_active_policy(
            POLICY_CODE, self.company_id, self._name,
        )

    def _adn_approval_amount(self, policy=None):
        """Return the discounted untaxed PO total in the policy currency."""
        self.ensure_one()
        policy = policy or self._adn_approval_policy()
        policy_currency = policy.currency_id or self.company_id.currency_id
        amount = self.amount_untaxed
        if self.currency_id != policy_currency:
            amount = self.currency_id._convert(
                amount, policy_currency, self.company_id,
                fields.Date.to_date(self.date_order) if self.date_order else fields.Date.context_today(self),
            )
        return policy, policy_currency.round(amount)

    def _adn_approval_snapshot(self, policy=None, policy_version=None):
        self.ensure_one()
        policy = policy or self._adn_approval_policy()
        policy, amount = self._adn_approval_amount(policy=policy)
        line_values = []
        for line in self.order_line.filtered(lambda item: not item.display_type).sorted("id"):
            values = {
                "line_id": line.id,
                "product_id": line.product_id.id,
                "description": line.name or "",
                "quantity": line.product_qty,
                "uom_id": line.product_uom_id.id,
                "unit_price": line.price_unit,
                "discount": getattr(line, "discount", 0.0),
                "untaxed_subtotal": line.price_subtotal,
                "planned_date": fields.Datetime.to_string(line.date_planned) if line.date_planned else False,
            }
            line_values.append(values)
        return {
            "policy_code": policy.code,
            "policy_version": policy_version if policy_version is not None else policy.policy_version,
            "purchase_order_id": self.id,
            "purchase_order_name": self.name,
            "company_id": self.company_id.id,
            "vendor_id": self.partner_id.id,
            "currency_id": self.currency_id.id,
            "policy_currency_id": (policy.currency_id or self.company_id.currency_id).id,
            "order_date": fields.Datetime.to_string(self.date_order) if self.date_order else False,
            "untaxed_total_source_currency": self.amount_untaxed,
            "approval_amount_policy_currency": amount,
            "lines": line_values,
        }

    def action_open_adn_approval_request(self):
        self.ensure_one()
        if not self.adn_approval_request_id:
            raise UserError(_("This purchase order has not been submitted for approval."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Purchase Order Approval"),
            "res_model": "adn.approval.request",
            "view_mode": "form",
            "res_id": self.adn_approval_request_id.id,
            "target": "current",
        }

    def _adn_sync_approval_fields(self, request):
        self.ensure_one()
        values = {"adn_approval_request_id": request.id}
        # Bypass this model's protected-field guard; values are generated server-side.
        super(PurchaseOrder, self).write(values)

    def action_submit_approval(self):
        if not self.env.user.has_group("adn_purchase_approval.group_purchase_approval_requester"):
            raise AccessError(_("You are not authorized to submit purchase orders for ADN approval."))
        for order in self:
            if order.state not in ("draft", "sent"):
                raise UserError(_("Only RFQs and draft purchase orders can be submitted for approval."))
            if not order.order_line:
                raise ValidationError(_("Add at least one purchase order line before submitting for approval."))
            if order.adn_approval_request_id and order.adn_approval_request_id.state in ("pending", "approved"):
                current_request = order.adn_approval_request_id
                snapshot = order._adn_approval_snapshot(
                    policy=current_request.policy_id,
                    policy_version=current_request.policy_version,
                )
                current_fingerprint = order.env["adn.approval.request"]._fingerprint(snapshot)
                if order.adn_approval_request_id.source_fingerprint == current_fingerprint:
                    raise UserError(_("This purchase order already has a current approval request."))
                order.adn_approval_request_id.action_supersede(
                    snapshot, _("Purchase order values changed before a new approval submission."),
                )
            policy, amount = order._adn_approval_amount()
            snapshot = order._adn_approval_snapshot()
            request = order.env["adn.approval.request"].submit(
                POLICY_CODE, order, amount, snapshot,
                reason=_('Purchase order approval for %s') % (order.name or order.display_name),
            )
            order._adn_sync_approval_fields(request)
            order.message_post(body=_("Submitted for ADN approval: %s (%s %s).") % (
                request.name, policy.currency_id.name, amount,
            ))
        return True

    def _adn_handle_approval_amendment(self, reason=None):
        for order in self.exists():
            request = order.adn_approval_request_id
            if not request or request.state not in ("pending", "approved"):
                continue
            snapshot = order._adn_approval_snapshot(
                policy=request.policy_id,
                policy_version=request.policy_version,
            )
            fingerprint = order.env["adn.approval.request"]._fingerprint(snapshot)
            if fingerprint == request.source_fingerprint:
                continue
            request.action_supersede(
                snapshot,
                reason or _("Approval-relevant purchase order values were amended; re-approval is required."),
            )
            # Related/computed fields follow the superseded request automatically.
            order.invalidate_recordset(["adn_approval_state", "adn_approval_tier", "adn_approval_fingerprint"])
            order.message_post(body=_("The previous approval was superseded because approval-relevant values changed. Submit the PO again."))

    def _adn_assert_approval_released(self):
        for order in self:
            request = order.adn_approval_request_id
            if not request:
                raise UserError(_("Purchase order %s requires approval. Submit it for approval before confirmation.") % order.display_name)
            snapshot = order._adn_approval_snapshot(
                policy=request.policy_id,
                policy_version=request.policy_version,
            )
            request.assert_released(order, POLICY_CODE, snapshot)
            if order.adn_approval_fingerprint != request.source_fingerprint:
                raise UserError(_("The purchase order approval fingerprint is stale. Submit the order for approval again."))

    def button_confirm(self, *args, **kwargs):
        self._adn_assert_approval_released()
        return super().button_confirm(*args, **kwargs)

    def button_approve(self, *args, **kwargs):
        self._adn_assert_approval_released()
        return super().button_approve(*args, **kwargs)

    def write(self, vals):
        protected = {
            "adn_approval_request_id", "adn_approval_state", "adn_approval_tier",
            "adn_approval_amount", "adn_approval_fingerprint", "adn_submitted_at",
            "adn_last_approval_at",
        }
        if protected.intersection(vals) and not self.env.su:
            raise AccessError(_("ADN approval fields are maintained by the approval workflow."))
        relevant = bool(APPROVAL_RELEVANT_PO_FIELDS.intersection(vals))
        if vals.get("state") == "purchase":
            if relevant:
                raise UserError(_("Amend the purchase order, resubmit it for approval, and confirm it in a separate action."))
            self._adn_assert_approval_released()
            for order in self:
                if not order._approval_allowed():
                    raise AccessError(_("You are not authorized under the standard Purchase approval policy to confirm this order."))
        result = super().write(vals)
        if relevant:
            self._adn_handle_approval_amendment()
        return result


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        orders = lines.mapped("order_id").filtered(lambda order: order.adn_approval_request_id)
        orders._adn_handle_approval_amendment()
        return lines

    def write(self, vals):
        relevant = bool(APPROVAL_RELEVANT_LINE_FIELDS.intersection(vals))
        orders = self.mapped("order_id") if relevant else self.env["purchase.order"]
        result = super().write(vals)
        if relevant:
            orders.exists()._adn_handle_approval_amendment()
        return result

    def unlink(self):
        orders = self.mapped("order_id")
        result = super().unlink()
        orders.exists()._adn_handle_approval_amendment()
        return result
