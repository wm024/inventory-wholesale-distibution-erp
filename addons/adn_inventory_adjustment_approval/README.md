# ADN Inventory Adjustment Approval — Odoo 19

**Version:** 19.0.1.0.0  
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

## 3. Valuation estimate

The approval basis is the absolute valuation difference, not sales price.

- Positive adjustment: company-specific product standard cost, or lot standard cost when lot valuation applies.
- Negative Standard/AVCO adjustment: company-specific product standard cost, or lot standard cost when lot valuation applies.
- Negative FIFO adjustment: calculate each quant line using the same cumulative per-product FIFO quantity context used by Odoo's `stock_account` valuation flow; lot-valuated products use lot standard cost, matching Odoo's lot-valuation branch.
- Non-valued locations and consigned stock excluded from valuation use zero value.
- The final aggregate is rounded using the company currency's rounding configuration.
- Requests are always split by accounting date to match Odoo's stock-accounting execution batches.

The addon stores the estimated approval value and the actual valuation value from the generated Odoo stock moves separately. FIFO valuation can change if unrelated stock valuation layers change between evaluation and execution; the request is recalculated before release, but concurrency against unrelated stock moves must still be tested in the target database.

## 4. DEC-003 is an activation gate

The approved FGA/TDD/RTM still identify DEC-003 as open: valuation basis/timing, aggregation across products, rounding, and approval routing require Operations/Finance confirmation. Therefore:

- The company-level approval switch defaults to **OFF**. The four DEC-003 configuration fields (aggregation, grouping, rounding and valuation timing) default to unset and are required before activation.
- The seeded approval policy and all approval rules default to **inactive**.
- The aggregation method and grouping mode are intentionally unset.
- Enabling the company switch without an active policy and completed configuration fails closed.

Recommended options supplied for the decision workshop:

| Setting | Option A | Option B |
|---|---|---|
| Aggregation | Sum absolute line values (prevents positive/negative offsets) | Absolute net value (allows offsets) |
| Request grouping | Separate by company and warehouse | One request per company; company/category and company/warehouse/category grouping are also supported. All modes split by accounting date. |
| Rounding | Company currency rounding after aggregate | Per-line rounding before aggregation |
| Multi-role tiers | All required in parallel | All required in ordered sequence |
| Valuation timing | Snapshot at submission and revalidate before release | Another Finance-approved timing rule |

The seeded approval rules reflect the FSD value tiers, but remain inactive:

| Absolute valuation difference | Required approver(s) |
|---|---|
| IDR 0–1,000,000 | Warehouse Supervisor |
| Above IDR 1,000,000–10,000,000 | Warehouse Manager |
| Above IDR 10,000,000–50,000,000 | Operations Manager + Finance Manager |
| Above IDR 50,000,000 | Managing Director + Finance Manager |

The seeded multi-role policy uses `all_required` with parallel steps as a conservative placeholder. Confirm the approval mode with Operations/Finance before activation.

## 5. Installation

Add this addon and the existing approval suite to the Odoo addons path, then update the app list and install:

```bash
./odoo-bin -d <database> -i adn_inventory_adjustment_approval --stop-after-init
```

The dependencies must be available in the addons path. For an existing environment where `adn_approval_core` is already installed, the new module can be installed independently.

## 6. Configuration before activation

1. Assign the Inventory Adjustment Requester group to authorized count users.
2. Assign Warehouse Supervisor, Warehouse Manager, Operations Manager, Finance Manager, and Managing Director approval groups to the correct users.
3. Assign Inventory Adjustment Executor to authorized inventory managers.
4. Confirm DEC-003 with Operations and Finance.
5. Set aggregation, request grouping (company, company/warehouse, company/category, or company/warehouse/category), rounding, and valuation timing on each company.
6. Activate the approval policy and only the approved rules; confirm the all-required/parallel mode or change it to the approved routing mode.
7. Set the company-level approval switch to ON.
8. Run the full boundary, valuation, access, and accounting regression suite in the target Odoo 19 database.

## 7. Security and enforcement

- Requesters can read their own requests; approvers and executors can read requests in their allowed companies.
- Snapshot lines are immutable for business users.
- Workflow links on `stock.quant` and `stock.move` cannot be set or changed by ordinary users.
- Both `action_apply_inventory()` and the lower-level `_apply_inventory()` path are guarded, including the inventory-report zero-quantity action.
- A forged release context is insufficient: release requires Inventory Manager membership, the exact approved quant set, an approved core request, a server-side release-in-progress state, and a matching current source fingerprint.
- Relevant changes to count quantities, quant identity, assigned counter, accounting date, reason, or evidence supersede the prior approval; evidence is copied to the request, checksum-verified, and read-only there.
- No manual transaction commits or custom stock/accounting ledger are introduced.

## 8. Tests

Automated tests included:
- Sum-of-absolute-lines aggregation.
- Absolute-net aggregation.
- Missing aggregation configuration.
- FSD approval tier boundaries.
- Per-line currency rounding.
- Default-disabled rollout and inactive policy safeguards.
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
- Multi-product, multi-warehouse, and multi-company grouping.
- Outdated counts and concurrent submissions.
- Stale approval after quantity/cost/lot changes.
- UI, import, and RPC attempts to bypass the gate.
- Evidence attachment copying, checksum integrity, and access after quant cleanup.
- Stock valuation and GL reconciliation for all five product categories.

## 9. Known limitations

- DEC-003 is not formally closed; production activation is intentionally blocked by default.
- No Odoo server/database was available in the build environment, so runtime installation and Odoo tests have not been executed.
- FIFO layer contention with unrelated stock moves requires target-database concurrency testing.
- The seeded approval policy's approval mode is a placeholder pending business confirmation.
