from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AdnApprovalRule(models.Model):
    _name = "adn.approval.rule"
    _description = "ADN Approval Rule"
    _order = "policy_id, sequence, id"

    policy_id = fields.Many2one("adn.approval.policy", required=True, ondelete="cascade", index=True)
    sequence = fields.Integer(default=10, required=True)
    has_min_amount = fields.Boolean(default=True)
    min_amount = fields.Monetary(currency_field="currency_id")
    has_max_amount = fields.Boolean(default=False)
    max_amount = fields.Monetary(currency_field="currency_id")
    currency_id = fields.Many2one(related="policy_id.currency_id", store=True, readonly=True)
    min_operator = fields.Selection([("gte", ">="), ("gt", ">")], default="gte", required=True)
    max_operator = fields.Selection([("lte", "<="), ("lt", "<")], default="lte", required=True)
    tier_code = fields.Char(required=True)
    approver_group_ids = fields.Many2many("res.groups", string="Approver Groups")
    required_approvals = fields.Integer(default=1, required=True)
    sequence_mode = fields.Selection([("parallel", "Parallel"), ("ordered", "Ordered")], default="ordered", required=True)
    requester_group_exclusions = fields.Many2many("res.groups", "adn_approval_rule_exclusion_rel", "rule_id", "group_id", string="Requester Group Exclusions")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("required_approvals_positive", "check(required_approvals > 0)", "Required approvals must be greater than zero."),
        ("amount_range_valid", "check(max_amount is null or min_amount is null or max_amount >= min_amount)", "Maximum amount must not be lower than minimum amount."),
        ("tier_policy_uniq", "unique(policy_id, tier_code)", "Tier code must be unique within a policy."),
    ]

    @api.constrains("approver_group_ids", "active")
    def _check_groups(self):
        for rec in self:
            if rec.active and not rec.approver_group_ids:
                raise ValidationError(_("Every active approval rule must have at least one approver group."))

    def matches_amount(self, amount):
        self.ensure_one()
        if self.has_min_amount:
            if self.min_operator == "gte" and amount < self.min_amount:
                return False
            if self.min_operator == "gt" and amount <= self.min_amount:
                return False
        if self.has_max_amount:
            if self.max_operator == "lte" and amount > self.max_amount:
                return False
            if self.max_operator == "lt" and amount >= self.max_amount:
                return False
        return True
