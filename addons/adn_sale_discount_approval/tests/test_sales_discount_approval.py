from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSalesDiscountApproval(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.policy = cls.env["adn.approval.policy"].create({
            "name": "Test Sales Discount Policy",
            "code": "SO_DISCOUNT_APPROVAL_TEST",
            "active": False,
            "source_model_id": cls.env.ref("sale.model_sale_order").id,
            "policy_version": 1,
            "approval_mode": "sequential",
        })
        cls.supervisor_rule = cls.env["adn.approval.rule"].create({
            "policy_id": cls.policy.id,
            "sequence": 10,
            "tier_code": "TEST_SUPERVISOR",
            "approver_group_ids": [(4, cls.env.ref("adn_sale_discount_approval.group_sales_supervisor_discount_approver").id)],
            "adn_has_min_discount": True,
            "adn_min_discount_percentage": 5.0,
            "adn_min_discount_operator": "gt",
            "adn_has_max_discount": True,
            "adn_max_discount_percentage": 10.0,
            "adn_max_discount_operator": "lte",
        })
        cls.manager_rule = cls.env["adn.approval.rule"].create({
            "policy_id": cls.policy.id,
            "sequence": 20,
            "tier_code": "TEST_MANAGER",
            "approver_group_ids": [(4, cls.env.ref("adn_sale_discount_approval.group_sales_manager_discount_approver").id)],
            "adn_has_min_discount": True,
            "adn_min_discount_percentage": 10.0,
            "adn_min_discount_operator": "gt",
            "adn_has_max_discount": True,
            "adn_max_discount_percentage": 15.0,
            "adn_max_discount_operator": "lte",
        })
        cls.director_rule = cls.env["adn.approval.rule"].create({
            "policy_id": cls.policy.id,
            "sequence": 30,
            "tier_code": "TEST_MANAGER_MD",
            "approver_group_ids": [
                (4, cls.env.ref("adn_sale_discount_approval.group_sales_manager_discount_approver").id),
                (4, cls.env.ref("adn_sale_discount_approval.group_managing_director_discount_approver").id),
            ],
            "adn_has_min_discount": True,
            "adn_min_discount_percentage": 15.0,
            "adn_min_discount_operator": "gt",
            "adn_has_max_discount": False,
        })

    def test_discount_threshold_boundaries(self):
        evaluator = self.env["sale.order"]
        cases = [
            (5.0, None),
            (5.01, self.supervisor_rule),
            (10.0, self.supervisor_rule),
            (10.01, self.manager_rule),
            (15.0, self.manager_rule),
            (15.01, self.director_rule),
        ]
        for percentage, expected in cases:
            matching = (self.supervisor_rule | self.manager_rule | self.director_rule).filtered(
                lambda rule: rule.matches_discount_percentage(percentage)
            )
            self.assertEqual(len(matching), 1 if expected else 0, "Unexpected tier for %s%%" % percentage)
            if expected:
                self.assertEqual(matching, expected)

    def test_mixed_line_order_uses_highest_applicable_tier(self):
        order_model = self.env["sale.order"]
        mixed_line_percentages = [8.0, 12.0, 6.5]
        highest = max(mixed_line_percentages)
        selected_rule = order_model._adn_discount_rule_for_percentage(self.policy, highest)
        self.assertEqual(selected_rule, self.manager_rule)
        self.assertEqual(len(self.director_rule.approver_group_ids), 2)

    def test_active_policy_requires_dec002_configuration(self):
        seeded_policy = self.env.ref("adn_sale_discount_approval.policy_so_discount_approval")
        with self.assertRaises(ValidationError):
            seeded_policy.write({"active": True})

    def test_explicit_discount_fails_closed_without_active_policy(self):
        partner = self.env["res.partner"].create({"name": "ADN Discount Test Customer"})
        product_template = self.env["product.template"].create({
            "name": "ADN Discount Test Product", "list_price": 100.0, "sale_ok": True,
        })
        product = product_template.product_variant_id
        order = self.env["sale.order"].create({
            "partner_id": partner.id,
            "order_line": [(0, 0, {
                "product_id": product.id,
                "product_uom_qty": 1.0,
                "product_uom_id": product.uom_id.id,
                "price_unit": 100.0,
            })],
        })
        order.order_line.write({"discount": 10.0})
        with self.assertRaises(UserError):
            order._adn_assert_discount_approval_released()
