from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError, UserError, ValidationError


class TestAdnApprovalEngine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.approver_group = cls.env.ref("adn_approval_core.group_approval_user")
        cls.manager_group = cls.env.ref("adn_approval_core.group_approval_manager")
        cls.requester = cls.env["res.users"].create({
            "name": "ADN Approval Requester", "login": "adn_approval_requester_test",
            "group_ids": [(6, 0, [cls.env.ref("base.group_user").id, cls.env.ref("adn_approval_core.group_approval_user").id])],
        })
        cls.approver = cls.env["res.users"].create({
            "name": "ADN Approval Approver", "login": "adn_approval_approver_test",
            "group_ids": [(6, 0, [cls.env.ref("base.group_user").id, cls.approver_group.id])],
        })
        cls.policy = cls.env["adn.approval.policy"].create({
            "name": "Test Policy", "code": "TEST_APPROVAL", "source_model_id": cls.env.ref("base.model_res_partner").id,
            "policy_version": 1, "approval_mode": "all_required", "effective_from": "2026-01-01",
        })
        cls.env["adn.approval.rule"].create({
            "policy_id": cls.policy.id, "sequence": 10, "min_amount": 0, "max_amount": 100000,
            "tier_code": "T1", "approver_group_ids": [(6, 0, [cls.approver_group.id])],
            "required_approvals": 1, "sequence_mode": "ordered",
        })
        cls.source = cls.env["res.partner"].create({"name": "Approval Source Test"})

    def test_submit_and_approve(self):
        Request = self.env["adn.approval.request"].with_user(self.requester)
        request = Request.submit("TEST_APPROVAL", self.source.with_user(self.requester), 2500, {"amount": 2500}, "Test reason")
        self.assertEqual(request.state, "pending")
        self.assertEqual(len(request.event_ids), 1)
        request.with_user(self.approver).action_approve("Reviewed")
        self.assertEqual(request.state, "approved")
        self.assertEqual(request.event_ids[-1].event_type, "approve")

    def test_requester_cannot_self_approve(self):
        request = self.env["adn.approval.request"].with_user(self.requester).submit(
            "TEST_APPROVAL", self.source.with_user(self.requester), 3000, {"amount": 3000}, "Test")
        with self.assertRaises(AccessError):
            request.with_user(self.requester).action_approve()

    def test_rejection_requires_reason(self):
        request = self.env["adn.approval.request"].with_user(self.requester).submit(
            "TEST_APPROVAL", self.source.with_user(self.requester), 3000, {"amount": 3000}, "Test")
        with self.assertRaises(ValidationError):
            request.with_user(self.approver).action_reject("")
        request.with_user(self.approver).action_reject("Insufficient justification")
        self.assertEqual(request.state, "rejected")

    def test_release_rejects_changed_snapshot(self):
        request = self.env["adn.approval.request"].with_user(self.requester).submit(
            "TEST_APPROVAL", self.source.with_user(self.requester), 3000, {"amount": 3000}, "Test")
        request.with_user(self.approver).action_approve()
        with self.assertRaises(UserError):
            request.assert_released(self.source, "TEST_APPROVAL", {"amount": 3001})

    def test_unassigned_approval_user_cannot_read_other_requests(self):
        request = self.env["adn.approval.request"].with_user(self.requester).submit(
            "TEST_APPROVAL", self.source.with_user(self.requester), 3000, {"amount": 3000}, "Test")
        unrelated_user = self.env["res.users"].create({
            "name": "Unassigned Approval User", "login": "adn_unassigned_approver_test",
            "group_ids": [(6, 0, [self.env.ref("base.group_user").id, self.env.ref("adn_approval_core.group_approval_user").id])],
        })
        visible = self.env["adn.approval.request"].with_user(unrelated_user).search([("id", "=", request.id)])
        self.assertFalse(visible)
        self.assertTrue(request.with_user(self.approver).exists())

    def test_client_context_cannot_bypass_lifecycle_protection(self):
        request = self.env["adn.approval.request"].with_user(self.requester).submit(
            "TEST_APPROVAL", self.source.with_user(self.requester), 3000, {"amount": 3000}, "Test")
        with self.assertRaises(AccessError):
            request.with_user(self.requester).with_context(approval_workflow=True).write({"state": "approved"})
        step = request.step_ids[:1]
        with self.assertRaises(AccessError):
            step.with_user(self.requester).with_context(approval_workflow=True).write({"decision": "approved"})
