from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAdnCreditRules(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.credit_service = cls.env["adn.credit.service"]

    def test_credit_utilization_boundaries(self):
        classify = self.credit_service._classify
        self.assertEqual(classify(800.0, 1000.0)[0], "normal")
        self.assertEqual(classify(800.01, 1000.0)[0], "warning")
        self.assertEqual(classify(1000.0, 1000.0)[0], "warning")
        self.assertEqual(classify(1000.01, 1000.0)[0], "hold")
        self.assertEqual(classify(800.0, 1000.0, warning_at_80=True)[0], "warning")
        self.assertEqual(classify(1000.0, 1000.0, hold_at_100=True)[0], "hold")

    def test_overdue_day_boundaries(self):
        bucket = self.credit_service._overdue_bucket
        self.assertEqual(bucket(0), "normal")
        self.assertEqual(bucket(1), "warning")
        self.assertEqual(bucket(30), "warning")
        self.assertEqual(bucket(31), "hold")
        self.assertEqual(bucket(60), "hold")

    def test_finance_block_is_absolute(self):
        decision, reasons = self.credit_service._classify(
            0.0, 100000000.0, finance_blocked=True,
        )
        self.assertEqual(decision, "blocked")
        self.assertIn("customer_finance_blocked", reasons)

    def test_zero_limit_fails_closed_for_positive_exposure(self):
        classify = self.credit_service._classify
        self.assertEqual(classify(0.0, 0.0)[0], "normal")
        self.assertEqual(classify(0.01, 0.0)[0], "hold")

    def test_multiple_hold_reasons_are_preserved(self):
        decision, reasons = self.credit_service._classify(
            1200.0, 1000.0, overdue_over_30=100.0,
        )
        self.assertEqual(decision, "hold")
        self.assertIn("invoice_overdue_more_than_30_days", reasons)
        self.assertIn("credit_exposure_over_100_percent", reasons)
