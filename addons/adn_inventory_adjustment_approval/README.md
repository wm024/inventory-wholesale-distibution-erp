# ADN Inventory Adjustment Approval — Odoo 19

**Version:** 19.0.1.0.1  
**Depends on:** `stock_account`, `mail`, `adn_approval_core`

## 1. Purpose

This addon adds a valuation-based approval gate to Odoo's standard physical inventory adjustment flow. It does not create a parallel inventory ledger. Odoo `stock.quant`, generated `stock.move` records, stock valuation, and accounting remain authoritative.

## 2. Functional scope

- Enter a reason on every changed count line or provide a specific reason in the inventory adjustment dialog; optional evidence files are copied onto the approval request for durable audit access.
- Snapshot the affected stock quants, quantities, valuation method, cost, and value.
- Aggregate the adjustment value using a company-level configured method.
- Route approval through `adn_approval_core`.
- Prevent standard inventory adjustment application while approval is pending or stale.
- Revalidate the count and valuation immediately before release.
- Apply the original Odoo inventory adjustment and link generated stock moves to the approval request.
- Retain immutable line snapshots and actual generated stock-move valuation.
- Supersede pending/approved requests when relevant count inputs are changed.

## 3. Valuation estimate and approved DEC-003 rules

The approval basis is the absolute valuation difference, not sales price. Each changed `stock.quant` adjustment line is valued from its signed quantity difference and the applicable Odoo inventory valuation unit cost.

- Positive adjustment: company-specific product standard cost, or lot standard cost when lot valuation applies.
- Negative Standard/AVCO adjustment: company-specific product standard cost, or lot standard cost when lot valuation applies.
- Negative FIFO adjustment: calculate each quant line using the same cumulative per-product FIFO quantity context used by Odoo's `stock_account` valuation flow; lot-valuated products use lot standard cost, matching Odoo's lot-valuation branch.
- Non-valued locations and consigned stock excluded from valuation use zero value.
- Round each changed adjustment line using the company currency precision, then sum the absolute rounded line values. Positive and negative lines both contribute and do not offset.
- Create one request per company + warehouse + accounting date. Product categories within the same warehouse/date are included together. Different warehouses, companies, and accounting dates are separate requests. A valued line without a resolvable warehouse is rejected.
- Snapshot valuation at submission and recalculate immediately before release. Any approval-relevant change supersedes the previous approval and requires a new request.
- Multi-role approval uses parallel steps and `all_required` policy semantics. Every listed role must approve, and the engine requires distinct approvers.
- Odoo's generated stock moves, valuation layers, and accounting entries remain authoritative; the addon does not create a parallel ledger.

DEC-003 was confirmed on **2026-11-22**. The approved IDR tiers are:

| Absolute valuation difference | Required approver(s) |
|---|---|
| IDR 0–1,000,000 | Warehouse Supervisor |
| Above IDR 1,000,000–10,000,000 | Warehouse Manager |
| Above IDR 10,000,000–50,000,000 | Operations Manager + Finance Manager |
| Above IDR 50,000,000 | Managing Director + Finance Manager |

The approval policy and rules are active in module data. The company-level enforcement switch remains **OFF** by default. Policy readiness is therefore separate from operational rollout.

## 4. Installation

Add this addon and the existing approval suite to the Odoo addons path, then update the app list and install:

```bash
./odoo-bin -d <database> -i adn_inventory_adjustment_approval --stop-after-init
```

The dependencies must be available in the addons path. For an existing environment where `adn_approval_core` is already installed, the new module can be installed independently.

For an existing installation of version `19.0.1.0.0`, upgrade the module to apply the DEC-003 migration (approved company settings and active approval policy/rules). The migration does not enable the company enforcement switch:

```bash
./odoo-bin -d <database> -u adn_inventory_adjustment_approval --stop-after-init
```

## 5. Configuration before activation

1. Assign the Inventory Adjustment Requester group to authorized count users.
2. Assign Warehouse Supervisor, Warehouse Manager, Operations Manager, Finance Manager, and Managing Director approval groups to the correct users.
3. Assign Inventory Adjustment Executor to authorized inventory managers.
4. Review the approved DEC-003 configuration and ensure warehouse/location mapping is complete. Confirm policy groups and assign distinct authorized users for Warehouse Supervisor, Warehouse Manager, Operations Manager, Finance Manager, and Managing Director.
6. Verify the active policy uses `all_required` and parallel steps; both roles in the two-role tiers must approve.
7. Run the full boundary, valuation, access, concurrency, and accounting regression suite in the target Odoo 19 database.
8. Enable the company-level approval switch only after UAT and operational sign-off.

## 6. Security and enforcement

- Requesters can read their own requests; approvers and executors can read requests in their allowed companies.
- Snapshot lines are immutable for business users.
- Workflow links on `stock.quant` and `stock.move` cannot be set or changed by ordinary users.
- Both `action_apply_inventory()` and the lower-level `_apply_inventory()` path are guarded, including the inventory-report zero-quantity action.
- A forged release context is insufficient: release requires Inventory Manager membership, the exact approved quant set, an approved core request, a server-side release-in-progress state, and a matching current source fingerprint.
- Relevant changes to count quantities, quant identity, assigned counter, accounting date, reason, or evidence supersede the prior approval; evidence is copied to the request, checksum-verified, and read-only there.
- No manual transaction commits or custom stock/accounting ledger are introduced.

## 7. Tests

Automated tests included:
- Sum-of-absolute-lines aggregation.
- Absolute-net aggregation.
- Missing aggregation configuration.
- FSD approval tier boundaries.
- Per-line currency rounding.
- Default-disabled enforcement switch, approved policy/routing, and company configuration safeguards.
- Company/warehouse/accounting-date grouping.
- Direct low-level inventory apply guard.
- Inventory-report zero-quantity action gate.
- Inventory-mode reason/evidence field handling.
- Fail-closed behavior when DEC-003 settings are incomplete.

Run in an Odoo 19 test database:

```bash
./odoo-bin -d <test_database> -i adn_inventory_adjustment_approval --test-enable --stop-after-init
```

Integration/UAT coverage still required:
- Standard and AVCO positive/negative adjustments.
- FIFO adjustments across multiple layers and products.
- Lot-valuated and consigned stock.
- Multi-product aggregation across categories within a warehouse/date; separate warehouse/company/accounting-date requests; missing warehouse mapping is rejected.
- Outdated counts and concurrent submissions.
- Stale approval after quantity/cost/lot changes.
- UI, import, and RPC attempts to bypass the gate.
- Evidence attachment copying, checksum integrity, and access after quant cleanup.
- Stock valuation and GL reconciliation for all five product categories.

## 8. Known limitations

- DEC-003 is approved and configured. Production enforcement remains disabled by default pending target-database runtime tests and UAT.
- No Odoo server/database was available in the build environment, so runtime installation and Odoo tests have not been executed.
- FIFO layer contention with unrelated stock moves requires target-database concurrency testing.
