# ADN Purchase Approval (Odoo 19)

**Technical version:** `19.0.1.0.0`  
**Depends on:** `purchase`, `adn_approval_core`  
**Baseline:** ADN-FSD-001 §6.5.3; ADN-TDD-001 §4.6, §4.7, §5.1; ADN-RTM-001 FSD-PUR-006–008 / TC-PUR-001–008  
**Customization:** CUS-002 — Purchase Order Approval

## 1. Scope

This addon extends the standard `purchase.order` model. It does not create a parallel purchase order, receipt, vendor bill, or payment model.

It implements:

- Tier selection from the untaxed purchase order total after line discounts.
- IDR policy thresholds and currency conversion to the policy currency where the PO currency differs.
- Submission to the shared `adn_approval_core` engine.
- Server-side confirmation guards on `button_confirm` and `button_approve`.
- Requester self-approval prevention through the shared approval engine.
- Approval invalidation when approval-relevant PO header or line values change.
- Retention of superseded approval requests and their audit events.
- Purchase-order form status and links to the approval request.

It does **not** implement three-way matching, vendor scorecards, internal purchase requisitions, or automated split-order blocking. Those are separate requirements/work packages.

## 2. Approval Matrix

The seed policy uses the approved FSD values:

| Untaxed PO amount after discounts (IDR) | Required approver |
|---:|---|
| IDR 0–10,000,000 inclusive | Procurement Supervisor |
| Above IDR 10,000,000–50,000,000 inclusive | Procurement Manager |
| Above IDR 50,000,000–150,000,000 inclusive | Operations Manager |
| Above IDR 150,000,000 | Managing Director |

All tiers require one approval from the assigned role. The policy is configured as ordered/sequential with one step per tier. This reflects the single required role in the FSD matrix; multi-role approval routing remains subject to the relevant business decision if the policy is changed.

**Amount basis:** `purchase.order.amount_untaxed`, which is Odoo's computed untaxed order amount after line discounts. Taxes and ancillary costs are excluded. The amount is converted to the policy currency (`IDR`) using the PO date and company conversion context.

## 3. Workflow

1. A purchase requester creates an RFQ/draft PO and completes its lines.
2. The requester selects **Submit for Approval**.
3. The adapter calculates the IDR approval amount and creates an immutable source snapshot/fingerprint through `adn_approval_core`.
4. The request is routed to the configured role for the applicable tier.
5. The approver opens the linked approval request and approves or rejects it. Rejection requires a reason in the shared engine.
6. The requester/authorized purchaser confirms the PO after approval.
7. The server re-computes the snapshot and blocks confirmation if the request is pending, rejected, superseded, belongs to another source record, or has a stale fingerprint.
8. Any relevant amendment supersedes the active/approved request. The PO must be submitted again.

## 4. Security Groups

Assign users explicitly:

- **Purchase Approval Requester** — purchase user access plus shared approval-user access; may submit PO requests.
- **Procurement Supervisor** — first-tier approver.
- **Procurement Manager** — second-tier approver.
- **Operations Manager — Purchase Approval** — third-tier approver.
- **Managing Director — Purchase Approval** — highest-tier approver.

Approver groups imply shared approval-user access and standard Purchase User access so approvers can read the source PO. Group assignment does not automatically grant PO confirmation rights beyond standard Odoo Purchase security.

Do not assign a requester to their own approval role where that would permit self-approval; the shared engine rejects approval by the request's requester regardless of group membership.

## 5. Installation

1. Place both `adn_approval_core` and `adn_purchase_approval` in an addons path.
2. Ensure Odoo 19 has the `purchase` application installed.
3. Ensure the target company currency and the approval policy currency are configured as IDR for the baseline. The adapter converts foreign-currency PO totals to the policy currency.
4. Update the Apps list.
5. Install `ADN Approval Core`, then `ADN Purchase Approval` (or install the latter and let Odoo resolve dependencies).
6. Assign the groups listed above to users.
7. Review the seeded policy and approval groups with Procurement and ERP governance before operational use.

Example:

```bash
./odoo-bin -d <database> -i adn_approval_core,adn_purchase_approval --stop-after-init
```

## 6. Amendment Fingerprint

The source snapshot includes company, vendor, PO currency, order date, source/policy currency, untaxed total, and line-level product, description, quantity, UoM, unit price, discount (when the installed Purchase model provides the field), untaxed subtotal, and planned date.

The adapter monitors relevant PO header writes and purchase-line create/write/unlink operations. A changed fingerprint supersedes the prior pending/approved request. Standard PO state is not duplicated or replaced.

## 7. Open Decision — DEC-001

The FSD/TDD explicitly leave the following unresolved:

- Delegation and approver substitution.
- Whether any special sequential/parallel behavior is needed beyond the one-role tier matrix.
- Amendment policy details beyond re-evaluation of value-affecting changes.
- Split-order detection keys, time window, false-positive handling, and exception process.

Delegation is not enabled. Split-order detection is not implemented as a hard block or heuristic. Add those only after Procurement records an approved decision and the affected tests are updated.

## 8. Verification Status and Limitations

Included automated tests cover tier boundaries, confirmation blocking while approval is pending, approval completion, and superseding an approved request after an amendment. Static Python/XML validation can be run without Odoo.

This package has **not** been installed or executed against a live Odoo 19 database in this environment. Before production/UAT, validate the exact Odoo 19 build, `purchase.order` method signatures, standard purchase double-validation configuration, installed field definitions, currency rates, view inheritance, and role mapping. The TDD itself requires those target-environment checks before treating hooks as validated.

The adapter also preserves standard Odoo Purchase double-validation authorization: the ADN approval does not replace the native `purchase.group_purchase_manager`/company threshold control. The user executing confirmation must satisfy both controls where native two-step approval is configured.
