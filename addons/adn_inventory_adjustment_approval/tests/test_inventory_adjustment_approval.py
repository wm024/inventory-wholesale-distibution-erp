import base64

from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestInventoryAdjustmentApproval(TransactionCase):

    def test_sum_absolute_lines_does_not_net_positive_and_negative_adjustments(self):
        request_model = self.env["adn.inventory.adjustment.request"]
        currency = self.env.ref("base.IDR")
        lines = [
            {"signed_value": 750000.0},
            {"signed_value": -500000.0},
        ]

        amount, signed_net = request_model._adn_aggregate_values(
            lines, "sum_absolute", currency, "aggregate",
        )

        self.assertEqual(amount, 1250000.0)
        self.assertEqual(signed_net, 250000.0)

    def test_absolute_net_mode_is_explicitly_different(self):
        request_model = self.env["adn.inventory.adjustment.request"]
        currency = self.env.ref("base.IDR")
        lines = [
            {"signed_value": 750000.0},
            {"signed_value": -500000.0},
        ]

        amount, signed_net = request_model._adn_aggregate_values(
            lines, "absolute_net", currency, "aggregate",
        )

        self.assertEqual(amount, 250000.0)
        self.assertEqual(signed_net, 250000.0)


    def test_per_line_rounding_is_applied_before_aggregation(self):
        request_model = self.env["adn.inventory.adjustment.request"]
        currency = self.env.ref("base.IDR")
        lines = [
            {"signed_value": 0.4},
            {"signed_value": 0.4},
        ]
        amount, signed_net = request_model._adn_aggregate_values(
            lines, "sum_absolute", currency, "per_line",
        )
        self.assertEqual(amount, 0.0)
        self.assertEqual(signed_net, 0.0)

    def test_aggregation_mode_is_required(self):
        with self.assertRaises(ValidationError):
            self.env["adn.inventory.adjustment.request"]._adn_aggregate_values(
                [{"signed_value": 100.0}], False, self.env.ref("base.IDR"), "aggregate",
            )

    def test_dec_003_policy_is_active_with_parallel_all_required_routing(self):
        policy = self.env.ref(
            "adn_inventory_adjustment_approval.policy_inventory_adjustment_approval"
        )
        self.assertTrue(policy.active)
        self.assertEqual(policy.approval_mode, "all_required")
        self.assertTrue(policy.rule_ids)
        self.assertFalse(policy.rule_ids.filtered(lambda rule: not rule.active))
        self.assertFalse(policy.rule_ids.filtered(lambda rule: rule.sequence_mode != "parallel"))
        operations_finance = policy.rule_ids.filtered(
            lambda rule: rule.tier_code == "INV_T3_OPERATIONS_FINANCE"
        )
        self.assertEqual(len(operations_finance.approver_group_ids), 2)
        self.assertEqual(operations_finance.required_approvals, 1)


    def test_approval_tier_boundaries_match_fsd(self):
        policy = self.env.ref(
            "adn_inventory_adjustment_approval.policy_inventory_adjustment_approval"
        )
        rules = {rule.tier_code: rule for rule in policy.rule_ids}
        cases = [
            (1_000_000, "INV_T1_WAREHOUSE_SUPERVISOR"),
            (1_000_001, "INV_T2_WAREHOUSE_MANAGER"),
            (10_000_000, "INV_T2_WAREHOUSE_MANAGER"),
            (10_000_001, "INV_T3_OPERATIONS_FINANCE"),
            (50_000_000, "INV_T3_OPERATIONS_FINANCE"),
            (50_000_001, "INV_T4_MD_FINANCE"),
        ]
        for amount, expected_tier in cases:
            matches = [rule.tier_code for rule in rules.values() if rule.matches_amount(amount)]
            self.assertEqual(matches, [expected_tier], amount)


    def _create_count_quant(self):
        company = self.env.company
        warehouse = self.env["stock.warehouse"].search(
            [("company_id", "=", company.id)], limit=1,
        )
        if not warehouse:
            warehouse = self.env["stock.warehouse"].create({
                "name": "ADN Inventory Approval Test Warehouse",
                "code": "ADN",
                "company_id": company.id,
            })
        product = self.env["product.product"].create({
            "name": "ADN Inventory Approval Test Product",
            "is_storable": True,
            "standard_price": 100.0,
        })
        quant = self.env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": product.id,
            "location_id": warehouse.lot_stock_id.id,
            "quantity": 1.0,
        })
        quant.action_set_inventory_quantity()
        quant.with_context(inventory_mode=True).write({"inventory_quantity": 2.0})
        return quant


    def test_inventory_mode_accepts_reason_and_evidence_fields(self):
        quant = self._create_count_quant()
        attachment = self.env["ir.attachment"].create({
            "name": "inventory-count-evidence.txt",
            "type": "binary",
            "datas": base64.b64encode(b"inventory count evidence"),
            "res_model": "stock.quant",
            "res_id": quant.id,
        })
        quant.with_context(inventory_mode=True).write({
            "adn_adjustment_reason": "Cycle count variance",
            "adn_adjustment_evidence_ids": [(4, attachment.id)],
        })
        self.assertEqual(quant.adn_adjustment_reason, "Cycle count variance")
        self.assertIn(attachment, quant.adn_adjustment_evidence_ids)


    def test_inventory_report_zero_action_uses_approval_gate(self):
        quant = self._create_count_quant()
        company = quant.company_id
        company.adn_inventory_adjustment_approval_enabled = True
        requester_group = self.env.ref(
            "adn_inventory_adjustment_approval.group_inventory_adjustment_requester"
        )
        self.env.user.write({"group_ids": [(4, requester_group.id)]})
        with self.assertRaises(ValidationError):
            with self.cr.savepoint():
                quant.with_context(inventory_report_mode=True).action_set_inventory_quantity_zero()
        self.assertEqual(quant.quantity, 1.0)

    def test_low_level_inventory_apply_is_blocked_when_company_gate_is_on(self):
        self.env.company.write({"adn_inventory_adjustment_approval_enabled": True})
        quant = self._create_count_quant()

        with self.assertRaises(UserError):
            quant._apply_inventory()

    def test_enabled_company_fails_closed_without_dec_003_configuration(self):
        requester_group = self.env.ref(
            "adn_inventory_adjustment_approval.group_inventory_adjustment_requester"
        )
        self.env.user.write({"group_ids": [(4, requester_group.id)]})
        self.env.company.write({
            "adn_inventory_adjustment_approval_enabled": True,
            "adn_inventory_adjustment_aggregation": False,
        })
        quant = self._create_count_quant()
        quant.write({"adn_adjustment_reason": "Cycle count variance"})

        with self.assertRaises(ValidationError):
            quant.action_apply_inventory()

        self.assertEqual(quant.quantity, 1.0)


    def test_default_grouping_is_company_warehouse_and_accounting_date(self):
        company = self.env.company
        company.write({
            "adn_inventory_adjustment_aggregation": "sum_absolute",
            "adn_inventory_adjustment_grouping": "company_warehouse",
            "adn_inventory_adjustment_rounding": "per_line",
            "adn_inventory_adjustment_valuation_timing": "submission_release",
        })
        quant = self._create_count_quant()
        grouped = self.env["stock.quant"]._adn_group_adjustment_quants(quant, company)
        self.assertEqual(len(grouped), 1)
        key = next(iter(grouped))
        self.assertEqual(key[0], company.id)
        self.assertEqual(key[1], quant.warehouse_id.id)
        self.assertFalse(key[2])
        self.assertEqual(key[3], quant.accounting_date)

    def test_company_dec_003_defaults_are_configured_but_enforcement_is_off(self):
        company = self.env["res.company"].create({"name": "ADN DEC-003 Defaults Test"})
        self.assertFalse(company.adn_inventory_adjustment_approval_enabled)
        self.assertEqual(company.adn_inventory_adjustment_aggregation, "sum_absolute")
        self.assertEqual(company.adn_inventory_adjustment_grouping, "company_warehouse")
        self.assertEqual(company.adn_inventory_adjustment_rounding, "per_line")
        self.assertEqual(
            company.adn_inventory_adjustment_valuation_timing, "submission_release"
        )
