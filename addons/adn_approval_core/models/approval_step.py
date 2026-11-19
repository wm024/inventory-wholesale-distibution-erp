from odoo import fields, models, _
from odoo.exceptions import AccessError, UserError


class AdnApprovalStep(models.Model):
    _name = "adn.approval.step"
    _description = "ADN Approval Step"
    _order = "request_id, sequence, id"

    request_id = fields.Many2one("adn.approval.request", required=True, ondelete="cascade", index=True)
    sequence = fields.Integer(required=True, default=10)
    approver_group_id = fields.Many2one("res.groups", required=True, ondelete="restrict")
    approver_id = fields.Many2one("res.users", ondelete="restrict")
    decision = fields.Selection([
        ("pending", "Pending"), ("approved", "Approved"),
        ("rejected", "Rejected"), ("skipped", "Skipped"),
    ], default="pending", required=True, index=True)
    decided_by_id = fields.Many2one("res.users", readonly=True)
    decided_at = fields.Datetime(readonly=True)
    comment = fields.Text(readonly=True)
    delegated_from_id = fields.Many2one("res.users", readonly=True)
    delegation_reference = fields.Char(readonly=True)

    def _record_decision(self, decision, comment=None):
        for step in self:
            request = step.request_id
            request._check_actor(step)
            if step.decision != "pending" or request.state != "pending":
                raise UserError(_("This approval step is no longer pending."))
            if decision == "rejected" and not comment:
                raise UserError(_("A rejection reason is required."))
            # Sequential rules only expose the first pending step to the action.
            vals = {
                "decision": decision, "decided_by_id": self.env.user.id,
                "decided_at": fields.Datetime.now(), "comment": comment or "",
            }
            step.sudo().write(vals)
        return True

    def write(self, vals):
        protected = {"decision", "decided_by_id", "decided_at", "comment", "delegated_from_id", "delegation_reference"}
        if protected.intersection(vals) and not self.env.su:
            raise AccessError(_("Approval decisions must be recorded through the approval workflow."))
        return super().write(vals)

    def unlink(self):
        if not self.env.su:
            raise AccessError(_("Approval steps are retained as audit evidence."))
        return super().unlink()
