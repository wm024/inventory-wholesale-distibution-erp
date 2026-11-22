from odoo import api, fields, models, _
from odoo.exceptions import AccessError, ValidationError


class AdnPartnerCredit(models.Model):
    _name = "adn.partner.credit"
    _description = "Customer Credit Profile"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "company_id, partner_id"
    _check_company_auto = True

    partner_id = fields.Many2one(
        "res.partner", required=True, ondelete="restrict", index=True,
        tracking=True,
    )
    commercial_partner_id = fields.Many2one(
        "res.partner", related="partner_id.commercial_partner_id", store=True, index=True,
    )
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company,
        index=True, ondelete="restrict",
    )
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id", store=True)
    credit_limit = fields.Monetary(
        currency_field="currency_id", tracking=True, required=True, default=0.0,
    )
    status = fields.Selection([
        ("normal", "Normal"), ("warning", "Warning"),
        ("hold", "Hold"), ("blocked", "Blocked"),
    ], required=True, default="normal", tracking=True, index=True)
    finance_blocked = fields.Boolean(string="Blocked by Finance", tracking=True)
    credit_limit_approved_by_id = fields.Many2one("res.users", readonly=True, copy=False)
    credit_limit_approval_request_id = fields.Many2one(
        "adn.approval.request", readonly=True, copy=False, ondelete="restrict",
        check_company=True,
    )
    review_date = fields.Date(string="Next Credit Review")
    proposed_credit_limit = fields.Monetary(currency_field="currency_id", copy=False)
    proposed_limit_reason = fields.Text(copy=False)
    limit_request_fingerprint = fields.Char(copy=False, readonly=True)
    evaluation_ids = fields.One2many("adn.credit.evaluation", "credit_profile_id")

    _partner_company_uniq = models.Constraint(
        "UNIQUE(commercial_partner_id, company_id)",
        "A customer can have only one credit profile per company.",
    )
    _credit_limit_nonnegative = models.Constraint(
        "CHECK(credit_limit >= 0)",
        "The approved credit limit cannot be negative.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.su:
            for vals in vals_list:
                if vals.get("credit_limit", 0.0):
                    raise AccessError(_(
                        "Initial approved credit limits must be loaded through the "
                        "controlled migration process or established through "
                        "credit-limit approval."
                    ))
                if {
                    "status", "credit_limit_approved_by_id", "credit_limit_approval_request_id",
                    "limit_request_fingerprint",
                }.intersection(vals):
                    raise AccessError(_(
                        "Credit status and approval audit fields cannot be supplied on creation."
                    ))
        partner_ids = {vals.get("partner_id") for vals in vals_list if vals.get("partner_id")}
        partners = self.env["res.partner"].browse(list(partner_ids)).mapped("commercial_partner_id")
        service = self.env["adn.credit.service"]
        for partner in partners.sorted("id"):
            service._lock_customer(partner)
        return super().create(vals_list)

    @api.constrains("partner_id")
    def _check_commercial_partner(self):
        for rec in self:
            if rec.partner_id != rec.partner_id.commercial_partner_id:
                raise ValidationError(_(
                    "Credit profiles must be assigned to the customer's commercial entity."
                ))

    def write(self, vals):
        protected = {
            "partner_id", "company_id", "status", "credit_limit_approved_by_id",
            "credit_limit_approval_request_id", "limit_request_fingerprint",
        }
        if protected.intersection(vals) and not self.env.su:
            raise AccessError(_("Credit status and approval audit fields are system-managed."))
        if "credit_limit" in vals and not self.env.su:
            if not self.env.user.has_group("adn_credit_control.group_credit_manager"):
                raise AccessError(_(
                    "Only Finance Credit Managers may maintain approved credit limits."
                ))
            if any(rec.credit_limit != vals["credit_limit"] for rec in self):
                raise AccessError(_(
                    "Credit limit changes must be submitted through the controlled "
                    "credit-limit approval workflow."
                ))
        if "finance_blocked" in vals and not self.env.su:
            if not self.env.user.has_group("adn_credit_control.group_credit_manager"):
                raise AccessError(_(
                    "Only Finance Credit Managers may block or unblock a customer."
                ))
            service = self.env["adn.credit.service"]
            for profile in self.sorted(lambda rec: rec.commercial_partner_id.id):
                service._lock_customer(profile.partner_id)
        return super().write(vals)

    def action_submit_credit_limit_change(self):
        self.ensure_one()
        if not self.env.user.has_group("adn_credit_control.group_credit_manager"):
            raise AccessError(_("Only Finance Credit Managers may request a credit limit change."))
        if self.proposed_credit_limit < 0 or self.proposed_credit_limit == self.credit_limit:
            raise ValidationError(_(
                "Enter a non-negative credit limit different from the current limit."
            ))
        if not self.proposed_limit_reason or not self.proposed_limit_reason.strip():
            raise ValidationError(_("A reason is required for a credit limit change."))
        company = self.company_id
        threshold_basis = company.adn_credit_limit_threshold_basis
        if not threshold_basis:
            raise ValidationError(_(
                "The credit-limit approval threshold basis is not configured. Resolve the "
                "TDD decision (IDR 100,000,000 applies to the increase or the resulting "
                "limit) before submitting."
            ))
        policy = self.env["adn.approval.policy"].get_active_policy(
            "CREDIT_LIMIT_CHANGE", company, "adn.partner.credit",
        )
        increase = max(self.proposed_credit_limit - self.credit_limit, 0.0)
        idr = self.env["res.currency"].search([("name", "=", "IDR")], limit=1)
        if not idr:
            raise ValidationError(_(
                "IDR currency is required to evaluate the credit-limit approval threshold."
            ))
        threshold = idr._convert(
            100000000.0, company.currency_id, company,
            self.env["adn.credit.service"]._company_today(company),
        )
        basis_amount = (
            increase if threshold_basis == "increase_amount"
            else self.proposed_credit_limit
        )
        tier_code = (
            "CREDIT_LIMIT_FINANCE_MD"
            if increase > 0 and basis_amount > threshold
            else "CREDIT_LIMIT_FINANCE_MANAGER"
        )
        rule = policy.rule_ids.filtered(lambda rec: rec.active and rec.tier_code == tier_code)[:1]
        if not rule:
            raise ValidationError(_("Credit-limit policy is missing active rule '%s'.") % tier_code)
        snapshot = {
            "profile_id": self.id,
            "partner_id": self.commercial_partner_id.id,
            "company_id": company.id,
            "old_limit": self.credit_limit,
            "new_limit": self.proposed_credit_limit,
            "threshold_basis": threshold_basis,
            "reason": self.proposed_limit_reason.strip(),
        }
        existing_request = self.credit_limit_approval_request_id
        if existing_request and existing_request.state in ("pending", "approved"):
            if existing_request.source_fingerprint == existing_request._fingerprint(snapshot):
                raise ValidationError(_(
                    "An active approval request already exists for this credit limit proposal."
                ))
            existing_request.action_supersede(
                snapshot,
                reason=_("Credit limit proposal changed; a new approval request is required."),
            )
        request = self.env["adn.approval.request"]._submit_with_rule(
            "CREDIT_LIMIT_CHANGE", self, increase, snapshot,
            reason=self.proposed_limit_reason.strip(),
            rule_override_id=rule.id,
            request_currency_id=company.currency_id.id,
        )
        self.sudo().write({
            "credit_limit_approval_request_id": request.id,
            "limit_request_fingerprint": request.source_fingerprint,
        })
        self.env["adn.credit.service"]._notify_approvers(
            request, company,
            _("A customer credit-limit change requires your review."),
        )
        return True

    def action_apply_approved_credit_limit(self):
        self.ensure_one()
        if not self.env.user.has_group("adn_credit_control.group_credit_manager"):
            raise AccessError(_("Only Finance Credit Managers may apply an approved credit limit."))
        self.env["adn.credit.service"]._lock_customer(self.partner_id)
        request = self.credit_limit_approval_request_id
        if not request or request.state != "approved":
            raise ValidationError(_("The credit limit change has not been approved."))
        snapshot = {
            "profile_id": self.id,
            "partner_id": self.commercial_partner_id.id,
            "company_id": self.company_id.id,
            "old_limit": self.credit_limit,
            "new_limit": self.proposed_credit_limit,
            "threshold_basis": self.company_id.adn_credit_limit_threshold_basis,
            "reason": (self.proposed_limit_reason or "").strip(),
        }
        request.assert_released(self, "CREDIT_LIMIT_CHANGE", snapshot)
        approved_steps = request.step_ids.filtered(lambda step: step.decision == "approved").sorted(
            lambda step: (step.sequence, step.id)
        )
        approver = approved_steps[-1].decided_by_id if approved_steps else self.env.user
        self.sudo().write({
            "credit_limit": self.proposed_credit_limit,
            "credit_limit_approved_by_id": approver.id,
            "proposed_credit_limit": 0.0,
            "proposed_limit_reason": False,
            "limit_request_fingerprint": False,
        })
        return True
