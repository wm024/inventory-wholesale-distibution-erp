from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AdnApprovalPolicy(models.Model):
    _inherit = "adn.approval.policy"

    adn_discount_reference_basis = fields.Selection([
        ("pricelist_unit_price", "Sales Order Line Unit Price Before Discount"),
        ("product_list_price", "Product Sales Price / List Price"),
        ("custom", "Custom Resolver (Developer Extension)"),
    ], string="Discount Reference Price Basis", copy=False, tracking=True)
    adn_discount_rounding_digits = fields.Selection(
        [(str(value), str(value)) for value in range(7)],
        string="Discount Percentage Rounding Digits", copy=False, tracking=True,
        help="Must be explicitly agreed under DEC-002 before activating this policy.",
    )
    adn_discount_rounding_method = fields.Selection([
        ("half_up", "Half Up"), ("half_even", "Half Even"), ("down", "Down"),
    ], string="Discount Rounding Method", copy=False, tracking=True)
    adn_discount_cumulative_mode = fields.Selection([
        ("single_standard_discount", "Single Standard Odoo Discount"),
        ("custom_resolver", "Custom / Cumulative Discount Resolver"),
    ], string="Cumulative Discount Treatment", copy=False, tracking=True)

    @api.constrains("code", "active", "source_model", "source_model_id", "adn_discount_reference_basis", "adn_discount_rounding_digits", "adn_discount_rounding_method", "adn_discount_cumulative_mode")
    def _check_discount_policy_configuration(self):
        for policy in self:
            if policy.code != "SO_DISCOUNT_APPROVAL" or not policy.active:
                continue
            if policy.source_model != "sale.order":
                raise ValidationError(_("Sales discount policy must target sale.order."))
            if not policy.adn_discount_reference_basis:
                raise ValidationError(_("Select the approved discount reference price basis before activating the policy (DEC-002)."))
            if policy.adn_discount_rounding_digits is False:
                raise ValidationError(_("Select discount percentage rounding precision under DEC-002 before activating the policy."))
            if not policy.adn_discount_rounding_method:
                raise ValidationError(_("Select the discount rounding method under DEC-002 before activating the policy."))
            if not policy.adn_discount_cumulative_mode:
                raise ValidationError(_("Select the cumulative discount treatment under DEC-002 before activating the policy."))
