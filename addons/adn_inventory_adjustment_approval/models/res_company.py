from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    adn_inventory_adjustment_approval_enabled = fields.Boolean(
        string="Require Inventory Adjustment Approval",
        default=False,
        help="When enabled, inventory count differences must be approved before application.",
    )
    adn_inventory_adjustment_aggregation = fields.Selection(
        [
            ("sum_absolute", "Sum of Absolute Line Values"),
            ("absolute_net", "Absolute Net Value"),
        ],
        string="Adjustment Approval Aggregation",
        help="Must be selected after DEC-003 is confirmed by Operations and Finance.",
    )
    adn_inventory_adjustment_grouping = fields.Selection(
        [
            ("company", "One Request per Company"),
            ("company_warehouse", "Separate by Company and Warehouse"),
            ("company_category", "Separate by Company and Product Category"),
            ("company_warehouse_category", "Separate by Company, Warehouse and Product Category"),
        ],
        string="Adjustment Approval Grouping",
        help="Must be selected after DEC-003 is confirmed by Operations and Finance.",
    )
    adn_inventory_adjustment_rounding = fields.Selection(
        [
            ("aggregate", "Round Final Aggregate"),
            ("per_line", "Round Each Line Before Aggregation"),
        ],
        string="Adjustment Approval Rounding",
        help="Must be selected after DEC-003 is confirmed by Operations and Finance.",
    )
    adn_inventory_adjustment_valuation_timing = fields.Selection(
        [("submission_release", "Snapshot at Submission and Revalidate Before Release")],
        string="Adjustment Valuation Snapshot Timing",
        help="Supported implementation baseline; confirm under DEC-003 before activation.",
    )
