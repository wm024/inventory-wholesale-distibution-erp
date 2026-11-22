from odoo import fields, models, _
from odoo.exceptions import UserError


class AdnCreditExceptionReason(models.TransientModel):
    _name = "adn.credit.exception.reason"
    _description = "Credit Exception Justification"

    sale_order_id = fields.Many2one("sale.order", required=True, readonly=True)
    reason = fields.Text(required=True)

    def action_submit(self):
        self.ensure_one()
        if not self.reason or not self.reason.strip():
            raise UserError(_("A business justification is required."))
        order = self.sale_order_id
        order.write({"adn_credit_exception_reason": self.reason.strip()})
        order.action_submit_credit_exception()
        return {"type": "ir.actions.act_window_close"}
