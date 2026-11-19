from odoo import fields, models, _
from odoo.exceptions import UserError


class AdnApprovalRejectWizard(models.TransientModel):
    _name = "adn.approval.reject.wizard"
    _description = "Reject Approval Request"

    request_id = fields.Many2one("adn.approval.request", required=True, readonly=True)
    reason = fields.Text(required=True)

    def action_confirm(self):
        self.ensure_one()
        if not self.reason or not self.reason.strip():
            raise UserError(_("A rejection reason is mandatory."))
        self.request_id.action_reject(self.reason.strip())
        return {"type": "ir.actions.act_window_close"}
