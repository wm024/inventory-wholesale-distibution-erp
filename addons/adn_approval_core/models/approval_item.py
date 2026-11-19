from odoo import fields, models, _
from odoo.exceptions import AccessError


class AdnApprovalItem(models.Model):
    _name = "adn.approval.item"
    _description = "ADN Approval Item"
    _order = "request_id, id"

    request_id = fields.Many2one("adn.approval.request", required=True, ondelete="cascade", index=True)
    source_line_model = fields.Char()
    source_line_res_id = fields.Integer(index=True)
    item_reference = fields.Char(required=True)
    basis_value = fields.Monetary(currency_field="currency_id")
    currency_id = fields.Many2one(related="request_id.currency_id", store=True, readonly=True)
    basis_percentage = fields.Float(digits=(16, 4))
    tier_code = fields.Char(required=True)
    state = fields.Selection([
        ("pending", "Pending"), ("approved", "Approved"),
        ("rejected", "Rejected"), ("not_required", "Not Required"),
    ], required=True, default="pending")
    snapshot = fields.Json(required=True, default=dict)

    def write(self, vals):
        if {"state", "snapshot", "source_line_model", "source_line_res_id"}.intersection(vals) and not self.env.su:
            raise AccessError(_("Approval item snapshots and decisions are controlled by workflow adapters."))
        return super().write(vals)

    def unlink(self):
        if not self.env.su:
            raise AccessError(_("Approval items are retained with their request."))
        return super().unlink()
