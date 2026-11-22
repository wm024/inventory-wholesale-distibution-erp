from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    adn_credit_control_enabled = fields.Boolean(
        string="Enable Customer Credit Control",
        default=False,
        help=(
            "Rollout switch. Enable only after the approved exposure basis and "
            "credit approval policies are configured."
        ),
    )
    adn_credit_commitment_basis = fields.Selection(
        [("order_total_less_posted_invoice_lines", "Order Total Less Posted Invoice Lines")],
        string="Credit Commitment Basis",
        help=(
            "DEC-006 gate. Select only after Finance approves how confirmed "
            "sales-order commitments overlap with posted receivables. The resolver "
            "subtracts posted invoice lines linked to the order."
        ),
    )
    adn_credit_trigger_point = fields.Selection(
        [("sale_order_confirmation", "Sales Order Confirmation")],
        string="Credit Validation Trigger",
        help=(
            "The current adapter validates before sale.order confirmation "
            "and direct state-to-sale writes."
        ),
    )
    adn_credit_exception_validity_start = fields.Selection(
        [("from_submission", "From Request Submission")],
        string="Credit Exception Validity Starts",
        help="The current adapter measures validity from exception request submission time.",
    )
    adn_credit_warning_boundary = fields.Selection(
        [
            ("above_80", "Warning Above 80% — Approved FSD/TDD"),
            ("at_80", "Warning At 80% — Project Rule"),
        ],
        string="Credit Warning Boundary",
        help=(
            "Resolve the project brief versus approved FSD boundary "
            "before enabling credit control."
        ),
    )
    adn_credit_hold_boundary = fields.Selection(
        [
            ("above_100", "Hold Above 100% — Approved FSD/TDD"),
            ("at_100", "Hold At 100% — Project Rule"),
        ],
        string="Credit Hold Boundary",
        help=(
            "Resolve the project brief versus approved FSD boundary "
            "before enabling credit control."
        ),
    )
    adn_credit_limit_threshold_basis = fields.Selection(
        [("increase_amount", "Amount of Increase"), ("new_limit", "New Credit Limit")],
        string="Credit Limit Approval Threshold Basis",
        help=(
            "TDD decision gate: Finance must confirm whether IDR 100,000,000 "
            "applies to the increase or the resulting limit."
        ),
    )
    adn_credit_exception_validity_hours = fields.Float(
        string="Credit Exception Validity (Hours)",
        help="DEC-006 gate. Must be approved by Finance; zero keeps exception release disabled.",
    )

    @api.constrains("adn_credit_exception_validity_hours")
    def _check_credit_exception_validity(self):
        for company in self:
            if company.adn_credit_exception_validity_hours < 0:
                raise ValidationError(_("Credit exception validity cannot be negative."))

    @api.constrains(
        "adn_credit_control_enabled", "adn_credit_commitment_basis",
        "adn_credit_trigger_point", "adn_credit_exception_validity_start",
        "adn_credit_warning_boundary", "adn_credit_hold_boundary",
        "adn_credit_limit_threshold_basis", "adn_credit_exception_validity_hours",
    )
    def _check_credit_control_activation(self):
        for company in self.filtered("adn_credit_control_enabled"):
            if not company.adn_credit_commitment_basis:
                raise ValidationError(_(
                    "Configure the Finance-approved credit commitment basis "
                    "before enabling credit control."
                ))
            if not company.adn_credit_trigger_point:
                raise ValidationError(_(
                    "Select the supported credit validation trigger before enabling credit control."
                ))
            if not company.adn_credit_exception_validity_start:
                raise ValidationError(_(
                    "Select the approved exception validity start point "
                    "before enabling credit control."
                ))
            if not company.adn_credit_warning_boundary or not company.adn_credit_hold_boundary:
                raise ValidationError(_(
                    "Select the approved warning and hold boundaries "
                    "before enabling credit control."
                ))
            if not company.adn_credit_limit_threshold_basis:
                raise ValidationError(_(
                    "Resolve the IDR 100,000,000 credit-limit threshold "
                    "basis before enabling credit control."
                ))
            if company.adn_credit_exception_validity_hours <= 0:
                raise ValidationError(_(
                    "Configure a positive credit exception validity before enabling credit control."
                ))
            policy_model = self.env["adn.approval.policy"].sudo()
            required_policies = [
                (
                    "CREDIT_EXCEPTION", "sale.order",
                    {
                        "CREDIT_FINANCE_MANAGER": {
                            "adn_credit_control."
                            "group_finance_manager_credit_approver"
                        },
                        "CREDIT_FINANCE_MD": {
                            "adn_credit_control.group_finance_manager_credit_approver",
                            "adn_credit_control."
                            "group_managing_director_credit_approver",
                        },
                    },
                ),
                (
                    "CREDIT_LIMIT_CHANGE", "adn.partner.credit",
                    {
                        "CREDIT_LIMIT_FINANCE_MANAGER": {
                            "adn_credit_control."
                            "group_finance_manager_credit_approver"
                        },
                        "CREDIT_LIMIT_FINANCE_MD": {
                            "adn_credit_control.group_finance_manager_credit_approver",
                            "adn_credit_control."
                            "group_managing_director_credit_approver",
                        },
                    },
                ),
            ]
            for code, source_model, expected_rules in required_policies:
                policy = policy_model.get_active_policy(code, company, source_model)
                if policy.approval_mode != "sequential":
                    raise ValidationError(_(
                        "Approval policy %s must use sequential approval." % code
                    ))
                for tier_code, group_xmlids in expected_rules.items():
                    rule = policy.rule_ids.filtered(
                        lambda rec: rec.active and rec.tier_code == tier_code
                    )
                    expected_group_ids = {self.env.ref(xmlid).id for xmlid in group_xmlids}
                    if (
                        len(rule) != 1
                        or set(rule.approver_group_ids.ids) != expected_group_ids
                        or rule.required_approvals != 1
                        or rule.sequence_mode != "ordered"
                    ):
                        raise ValidationError(_(
                            "Approval policy %(policy)s tier %(tier)s must have the "
                            "approved approver groups, "
                            "one approval per step, and ordered sequencing.",
                            policy=code, tier=tier_code,
                        ))
