from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AdnApprovalPolicy(models.Model):
    _name = "adn.approval.policy"
    _description = "ADN Approval Policy"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "code, company_id"

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(required=True, index=True, copy=False, tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    company_id = fields.Many2one("res.company", index=True, tracking=True)
    source_model_id = fields.Many2one("ir.model", required=True, ondelete="restrict")
    source_model = fields.Char(related="source_model_id.model", store=True, readonly=True)
    policy_version = fields.Integer(required=True, default=1, tracking=True)
    currency_id = fields.Many2one("res.currency")
    approval_mode = fields.Selection([
        ("all_required", "All Required"),
        ("any_required", "Any Required"),
        ("sequential", "Sequential"),
    ], required=True, default="sequential", tracking=True)
    effective_from = fields.Date(required=True, default=fields.Date.context_today)
    effective_to = fields.Date()
    notes = fields.Text()
    rule_ids = fields.One2many("adn.approval.rule", "policy_id", string="Approval Rules")

    _sql_constraints = [
        ("code_company_uniq", "unique(code, company_id)", "The policy code must be unique per company."),
        ("version_positive", "check(policy_version > 0)", "Policy version must be greater than zero."),
    ]

    @api.constrains("effective_from", "effective_to")
    def _check_effective_dates(self):
        for rec in self:
            if rec.effective_to and rec.effective_to < rec.effective_from:
                raise ValidationError(_("The effective end date cannot be earlier than the start date."))

    def action_increment_version(self):
        for rec in self:
            rec.write({"policy_version": rec.policy_version + 1})
        return True

    @api.model
    def get_active_policy(self, code, company, source_model):
        today = fields.Date.context_today(self)
        domain = [
            ("code", "=", code), ("active", "=", True),
            ("source_model", "=", source_model),
            ("effective_from", "<=", today),
            "|", ("effective_to", "=", False), ("effective_to", ">=", today),
            "|", ("company_id", "=", company.id), ("company_id", "=", False),
        ]
        company = company or self.env.company
        policies = self.search(domain)
        if len(policies) > 1:
            company_policy = policies.filtered(lambda p: p.company_id == company)
            policies = company_policy or policies.filtered(lambda p: not p.company_id)
        if len(policies) != 1:
            raise ValidationError(_("Expected exactly one active policy '%s' for model '%s'; found %s.") % (code, source_model, len(policies)))
        return policies
