from odoo import fields, models, _
from odoo.exceptions import AccessError


class AdnApprovalEvent(models.Model):
    _name = "adn.approval.event"
    _description = "ADN Approval Audit Event"
    _order = "event_at desc, id desc"

    request_id = fields.Many2one("adn.approval.request", required=True, ondelete="restrict", index=True)
    event_type = fields.Selection([
        ("submit", "Submitted"), ("approve", "Approved"), ("reject", "Rejected"),
        ("cancel", "Cancelled"), ("amend", "Amended"), ("supersede", "Superseded"),
        ("release", "Released"), ("expire", "Expired"),
    ], required=True, index=True)
    event_at = fields.Datetime(required=True, default=fields.Datetime.now, readonly=True, index=True)
    actor_id = fields.Many2one("res.users", required=True, readonly=True, default=lambda self: self.env.user)
    previous_state = fields.Char()
    new_state = fields.Char()
    comment = fields.Text()
    payload_snapshot = fields.Json(default=dict)

    def write(self, vals):
        raise AccessError(_("Approval audit events are append-only and cannot be modified."))

    def unlink(self):
        raise AccessError(_("Approval audit events cannot be deleted."))
