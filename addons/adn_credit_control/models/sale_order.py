from odoo import fields, models, _
from odoo.exceptions import AccessError, UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    adn_credit_evaluation_id = fields.Many2one(
        "adn.credit.evaluation", readonly=True, copy=False, ondelete="restrict", check_company=True,
        groups=(
            "adn_credit_control.group_credit_manager,"
            "adn_credit_control.group_finance_manager_credit_approver,"
            "adn_credit_control.group_managing_director_credit_approver"
        ),
    )
    adn_credit_approval_request_id = fields.Many2one(
        "adn.approval.request", readonly=True, copy=False, ondelete="restrict", check_company=True,
    )
    adn_credit_decision = fields.Selection([
        ("normal", "Normal"), ("warning", "Warning"),
        ("hold", "Hold"), ("blocked", "Blocked"),
    ], readonly=True, copy=False)
    adn_credit_exposure = fields.Monetary(
        currency_field="company_currency_id", readonly=True, copy=False,
        groups=(
            "adn_credit_control.group_credit_manager,"
            "adn_credit_control.group_finance_manager_credit_approver,"
            "adn_credit_control.group_managing_director_credit_approver"
        ),
    )
    adn_credit_available = fields.Monetary(
        currency_field="company_currency_id", readonly=True, copy=False,
        groups=(
            "adn_credit_control.group_credit_manager,"
            "adn_credit_control.group_finance_manager_credit_approver,"
            "adn_credit_control.group_managing_director_credit_approver"
        ),
    )
    adn_credit_utilization = fields.Float(
        digits=(16, 4), readonly=True, copy=False,
        groups=(
            "adn_credit_control.group_credit_manager,"
            "adn_credit_control.group_finance_manager_credit_approver,"
            "adn_credit_control.group_managing_director_credit_approver"
        ),
    )
    adn_credit_exception_reason = fields.Text(copy=False)
    adn_credit_conversion_date = fields.Date(readonly=True, copy=False)
    adn_credit_exception_revision = fields.Integer(readonly=True, copy=False, default=0)
    company_currency_id = fields.Many2one(related="company_id.currency_id", readonly=True)

    def _adn_credit_exception_snapshot(self, result):
        self.ensure_one()
        return {
            "source_fingerprint": result["fingerprint"],
            "exception_revision": self.adn_credit_exception_revision,
            "reason": (self.adn_credit_exception_reason or "").strip(),
            "validity_hours": self.company_id.adn_credit_exception_validity_hours,
            "validity_start": self.company_id.adn_credit_exception_validity_start,
            "trigger_point": self.company_id.adn_credit_trigger_point,
        }

    def _adn_credit_supersede_stale_request(self, request, result):
        self.ensure_one()
        snapshot = self._adn_credit_exception_snapshot(result)
        if not request or request.state not in ("pending", "approved"):
            return False
        expired = bool(request.valid_until and request.valid_until < fields.Datetime.now())
        if request.source_fingerprint == request._fingerprint(snapshot) and not expired:
            return False
        next_revision = self.adn_credit_exception_revision + 1
        snapshot["exception_revision"] = next_revision
        request.action_supersede(
            snapshot,
            reason=_(
                "Credit exposure or source values changed, or the exception expired; "
                "resubmission is required."
            ),
        )
        self.sudo().write({
            "adn_credit_exception_revision": next_revision,
            "adn_credit_approval_request_id": False,
        })
        return True

    def _adn_post_credit_warning(self, result):
        self.ensure_one()
        recipient_partner_ids = set()
        if self.user_id.partner_id:
            recipient_partner_ids.add(self.user_id.partner_id.id)
        if result["overdue_1_30"] > 0:
            finance_group = self.env.ref(
                "adn_credit_control.group_finance_manager_credit_approver"
            )
            finance_users = self.env["res.users"].sudo().search([
                ("group_ids", "in", finance_group.id),
                ("company_ids", "in", self.company_id.id),
                ("active", "=", True),
                ("share", "=", False),
            ])
            recipient_partner_ids.update(finance_users.mapped("partner_id").ids)
        self.message_post(
            body=_(
                "Credit warning: the customer has reached the configured credit warning "
                "threshold or has an invoice overdue by 1–30 calendar days. "
                "Finance review may be required."
            ),
            partner_ids=sorted(recipient_partner_ids),
        )

    def _adn_credit_check_and_lock(self):
        self.ensure_one()
        if (
            not self.partner_id
            or self.state not in ("draft", "sent")
            or not self.company_id.adn_credit_control_enabled
        ):
            return True
        service = self.env["adn.credit.service"]
        service._lock_customer(self.partner_id)
        result = service._evaluate(self)
        if result["decision"] == "blocked":
            raise UserError(_(
                "This customer is blocked by Finance. Credit order confirmation is prohibited."
            ))
        request = self.adn_credit_approval_request_id
        if result["decision"] in ("normal", "warning"):
            self._adn_credit_supersede_stale_request(request, result)
            result["evaluation"].sudo().write({
                "released_at": fields.Datetime.now(),
                "released_by_id": self.env.user.id,
            })
            if result["decision"] == "warning":
                self._adn_post_credit_warning(result)
            return True

        if request and request.state == "approved":
            if request.valid_until and request.valid_until < fields.Datetime.now():
                raise UserError(_(
                    "The credit exception approval has expired. Submit a new exception request."
                ))
            request.assert_released(
                self, "CREDIT_EXCEPTION", self._adn_credit_exception_snapshot(result),
            )
            result["evaluation"].sudo().write({
                "approval_request_id": request.id,
                "released_at": fields.Datetime.now(),
                "released_by_id": self.env.user.id,
            })
            return True
        if request and request.state == "pending":
            raise UserError(_(
                "Credit exception approval is pending. The sales order cannot be confirmed."
            ))
        if request and request.state in ("rejected", "superseded", "cancelled"):
            raise UserError(_(
                "The credit exception is no longer valid. Review the order "
                "and submit a new request."
            ))
        raise UserError(_(
            "Credit hold: this order requires Finance approval. Add a business justification "
            "and submit a credit exception request before confirmation."
        ))

    def action_open_credit_exception_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Submit Credit Exception"),
            "res_model": "adn.credit.exception.reason",
            "view_mode": "form",
            "target": "new",
            "context": {"default_sale_order_id": self.id},
        }

    def action_submit_credit_exception(self):
        if not self.env.user.has_group("adn_credit_control.group_credit_requester"):
            raise AccessError(_("You are not authorized to submit credit exception requests."))
        for order in self:
            if not order.company_id.adn_credit_control_enabled:
                raise UserError(_("Customer Credit Control is not enabled for this company."))
            if order.state not in ("draft", "sent"):
                raise UserError(_("Credit exceptions can only be submitted for draft quotations."))
            service = self.env["adn.credit.service"]
            service._lock_customer(order.partner_id)
            result = service._evaluate(order)
            if result["decision"] not in ("hold", "blocked"):
                raise UserError(_("The current credit evaluation does not require an exception."))
            if result["decision"] == "blocked":
                raise UserError(_(
                    "Finance-blocked customers cannot be released through a transaction exception."
                ))
            existing_request = order.adn_credit_approval_request_id
            next_revision = order.adn_credit_exception_revision + 1
            if existing_request and existing_request.state in ("pending", "approved"):
                current_snapshot = order._adn_credit_exception_snapshot(result)
                expired = bool(
                    existing_request.valid_until
                    and existing_request.valid_until < fields.Datetime.now()
                )
                same_snapshot = (
                    existing_request.source_fingerprint
                    == existing_request._fingerprint(current_snapshot)
                )
                if same_snapshot and not expired:
                    raise UserError(_(
                        "An active credit exception request already exists for this order."
                    ))
                current_snapshot["exception_revision"] = next_revision
                existing_request.action_supersede(
                    current_snapshot,
                    reason=_(
                        "Credit exposure or source values changed, or the exception expired; "
                        "resubmission is required."
                    ),
                )
            order.sudo().write({"adn_credit_exception_revision": next_revision})
            self.env["adn.credit.service"]._submit_exception(
                order, order.adn_credit_exception_reason, result,
            )
            order.message_post(body=_("Credit exception approval has been submitted to Finance."))
        return True

    def write(self, vals):
        if vals.get("state") in ("sale", "done") and not self.env.su:
            candidates = self.filtered(lambda rec: rec.state in ("draft", "sent"))
            customer_ids = candidates.mapped("partner_id.commercial_partner_id").ids
            if len(customer_ids) < len(candidates):
                raise UserError(_(
                    "Confirm credit-controlled orders for the same customer one at a time "
                    "so each order is evaluated against the latest exposure."
                ))
            for order in candidates.sorted(key=lambda rec: rec.partner_id.commercial_partner_id.id):
                order._adn_credit_check_and_lock()
        protected = {
            "adn_credit_evaluation_id", "adn_credit_approval_request_id",
            "adn_credit_decision", "adn_credit_exposure",
            "adn_credit_available", "adn_credit_utilization",
            "adn_credit_conversion_date", "adn_credit_exception_revision",
        }
        if protected.intersection(vals) and not self.env.su:
            raise AccessError(_("Credit control audit fields are system-managed."))
        return super().write(vals)
