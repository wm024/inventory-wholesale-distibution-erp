from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestAdnPurchaseApproval(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.requester_group = cls.env.ref("adn_purchase_approval.group_purchase_approval_requester")
        cls.supervisor_group = cls.env.ref("adn_purchase_approval.group_procurement_supervisor")
        cls.requester = cls.env["res.users"].create({
            "name": "ADN PO Requester",
            "login": "adn_po_requester_test",
            "company_id": cls.company.id,
            "company_ids": [(6, 0, [cls.company.id])],
            "group_ids": [(6, 0, [cls.env.ref("base.group_user").id, cls.requester_group.id])],
        })
        cls.supervisor = cls.env["res.users"].create({
            "name": "ADN PO Supervisor",
            "login": "adn_po_supervisor_test",
            "company_id": cls.company.id,
            "company_ids": [(6, 0, [cls.company.id])],
            "group_ids": [(6, 0, [cls.env.ref("base.group_user").id, cls.supervisor_group.id])],
        })
        cls.vendor = cls.env["res.partner"].create({
            "name": "ADN Test Vendor", "company_id": False, "supplier_rank": 1,
        })
        cls.product = cls.env["product.product"].create({
            "name": "ADN Test Purchase Product", "type": "consu", "purchase_ok": True,
        })
        cls.policy = cls.env.ref("adn_purchase_approval.policy_po_approval")

    def _make_order(self, price=100000):
        return self.env["purchase.order"].with_user(self.requester).create({
            "partner_id": self.vendor.id,
            "company_id": self.company.id,
            "currency_id": self.company.currency_id.id,
            "order_line": [(0, 0, {
                "product_id": self.product.id,
                "name": self.product.display_name,
                "product_qty": 1.0,
                "product_uom_id": self.product.uom_id.id,
                "price_unit": price,
                "date_planned": "2026-12-01 00:00:00",
            })],
        })

    def test_purchase_tier_boundaries(self):
        rules = self.policy.rule_ids
        self.assertEqual(len(rules), 4)
        self.assertTrue(rules.filtered(lambda r: r.tier_code == "PO_T1_SUPERVISOR").matches_amount(10000000))
        self.assertTrue(rules.filtered(lambda r: r.tier_code == "PO_T2_PROCUREMENT_MANAGER").matches_amount(10000001))
        self.assertTrue(rules.filtered(lambda r: r.tier_code == "PO_T2_PROCUREMENT_MANAGER").matches_amount(50000000))
        self.assertTrue(rules.filtered(lambda r: r.tier_code == "PO_T3_OPERATIONS_MANAGER").matches_amount(50000001))
        self.assertTrue(rules.filtered(lambda r: r.tier_code == "PO_T3_OPERATIONS_MANAGER").matches_amount(150000000))
        self.assertTrue(rules.filtered(lambda r: r.tier_code == "PO_T4_MANAGING_DIRECTOR").matches_amount(150000001))

    def test_confirmation_is_blocked_until_approval(self):
        order = self._make_order()
        order.action_submit_approval()
        self.assertEqual(order.adn_approval_state, "pending")
        with self.assertRaises(UserError):
            order.button_confirm()

    def test_direct_state_write_cannot_bypass_approval(self):
        order = self._make_order()
        with self.assertRaises(UserError):
            order.write({"state": "purchase"})

    def test_approval_and_amendment_supersedes_previous_request(self):
        order = self._make_order()
        order.action_submit_approval()
        request = order.adn_approval_request_id
        request.with_user(self.supervisor).action_approve("Reviewed against purchase requirement")
        self.assertEqual(request.state, "approved")
        self.assertEqual(order.adn_approval_state, "approved")
        order.order_line.with_user(self.requester).write({"price_unit": 125000})
        self.assertEqual(request.state, "superseded")
        self.assertEqual(order.adn_approval_state, "superseded")
