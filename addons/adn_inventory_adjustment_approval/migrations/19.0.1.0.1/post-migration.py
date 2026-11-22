from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Apply the confirmed DEC-003 baseline to every existing company. This
    # intentionally replaces any pre-approval decision settings. The
    # enforcement switch is deliberately not enabled by this migration.
    defaults = {
        "adn_inventory_adjustment_aggregation": "sum_absolute",
        "adn_inventory_adjustment_grouping": "company_warehouse",
        "adn_inventory_adjustment_rounding": "per_line",
        "adn_inventory_adjustment_valuation_timing": "submission_release",
    }
    companies = env["res.company"].with_context(active_test=False).search([])
    if companies:
        companies.write(defaults)

    policy = env.ref(
        "adn_inventory_adjustment_approval.policy_inventory_adjustment_approval",
        raise_if_not_found=False,
    )
    if policy:
        policy.write({
            "active": True,
            "approval_mode": "all_required",
            "policy_version": max(policy.policy_version + 1, 2),
            "notes": (
                "DEC-003 approved 2026-11-22: sum absolute per-line valuation values "
                "after company-currency rounding; group by company, warehouse and "
                "accounting date; snapshot at submission and revalidate before release; "
                "all listed roles approve in parallel. Company enforcement remains "
                "disabled until UAT sign-off. IDR tiers follow FSD §6.7.7."
            ),
        })
        policy.rule_ids.write({"active": True, "sequence_mode": "parallel"})
