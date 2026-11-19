from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AdnApprovalRule(models.Model):
    _inherit = "adn.approval.rule"

    adn_has_min_discount = fields.Boolean(default=True)
    adn_min_discount_percentage = fields.Float(digits=(16, 6))
    adn_min_discount_operator = fields.Selection([("gte", ">="), ("gt", ">")], default="gt")
    adn_has_max_discount = fields.Boolean(default=False)
    adn_max_discount_percentage = fields.Float(digits=(16, 6))
    adn_max_discount_operator = fields.Selection([("lte", "<="), ("lt", "<")], default="lte")

    @api.constrains("policy_id", "adn_has_min_discount", "adn_min_discount_percentage", "adn_min_discount_operator", "adn_has_max_discount", "adn_max_discount_percentage", "adn_max_discount_operator")
    def _check_discount_range(self):
        for rule in self:
            if rule.policy_id.code != "SO_DISCOUNT_APPROVAL":
                continue
            if rule.adn_has_min_discount and rule.adn_has_max_discount and rule.adn_max_discount_percentage < rule.adn_min_discount_percentage:
                raise ValidationError(_("Maximum discount percentage cannot be lower than the minimum."))

    def matches_discount_percentage(self, percentage):
        self.ensure_one()
        if self.adn_has_min_discount:
            if self.adn_min_discount_operator == "gte" and percentage < self.adn_min_discount_percentage:
                return False
            if self.adn_min_discount_operator == "gt" and percentage <= self.adn_min_discount_percentage:
                return False
        if self.adn_has_max_discount:
            if self.adn_max_discount_operator == "lte" and percentage > self.adn_max_discount_percentage:
                return False
            if self.adn_max_discount_operator == "lt" and percentage >= self.adn_max_discount_percentage:
                return False
        return True
