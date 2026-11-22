from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    adn_credit_profile_ids = fields.One2many(
        "adn.partner.credit", "partner_id", string="Credit Profiles",
    )
