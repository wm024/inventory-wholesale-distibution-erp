from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class StockMove(models.Model):
    _inherit = "stock.move"

    adn_inventory_adjustment_request_id = fields.Many2one(
        "adn.inventory.adjustment.request", string="ADN Inventory Adjustment Request",
        readonly=True, copy=False, index=True, ondelete="restrict", check_company=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        linked_request_ids = {
            vals["adn_inventory_adjustment_request_id"]
            for vals in vals_list
            if vals.get("adn_inventory_adjustment_request_id")
        }
        if linked_request_ids:
            if not self.env.context.get("adn_inventory_approval_release"):
                raise AccessError(_("The ADN inventory adjustment request link is maintained by the workflow."))
            if not self.env.user.has_group("adn_inventory_adjustment_approval.group_inventory_adjustment_executor"):
                raise AccessError(_("Only an Inventory Manager may create moves for an approved adjustment."))
            context_request_id = self.env.context.get("adn_inventory_approval_request_id")
            requests = self.env["adn.inventory.adjustment.request"].browse(linked_request_ids).exists()
            requests.invalidate_recordset(["state", "approval_state", "release_in_progress"])
            if (
                len(requests) != 1
                or requests.id != context_request_id
                or requests.state != "submitted"
                or requests.approval_state != "approved"
                or not requests.release_in_progress
            ):
                raise AccessError(_("Stock moves can only be linked during an approved request release."))
        return super().create(vals_list)

    def write(self, vals):
        if "adn_inventory_adjustment_request_id" in vals:
            raise AccessError(_("The ADN inventory adjustment request link is maintained by the workflow."))
        return super().write(vals)
