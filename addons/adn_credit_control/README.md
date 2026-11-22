# ADN Customer Credit Control — Odoo 19

## Scope

Implements the FSD-CRD / FGA CUS-004 / TDD §5.3 credit-control adapter using standard Odoo accounting and sales records.

- Customer credit profiles are company-specific and use the company's currency.
- Posted customer invoice receivable residuals are read from `account.move.line`.
- Open confirmed sales orders are read from `sale.order` and linked invoice lines.
- No duplicate AR ledger or manually maintained outstanding balance is created.
- Every successful evaluation is stored as an immutable snapshot with Finance-only source details.
- Sales Representatives are notified on warnings; Finance Manager approvers are also notified when an invoice is 1–30 calendar days overdue. Routed approvers receive notifications for credit exceptions and credit-limit changes. Sales users can submit transaction-specific exception requests; detailed exposure is Finance-only.
- Confirmation is enforced in the ORM `write({'state': 'sale'})` path used by Odoo 19 `sale.order.action_confirm`, not only by a UI button.
- A parameterized PostgreSQL `SELECT ... FOR UPDATE` on the customer's commercial partner serializes credit-consuming confirmations, approved limit application, profile creation, and Finance block/unblock actions. This is the only raw SQL operation; it is used solely for row locking, not CRUD. Multi-order confirmation for the same customer is rejected; confirm those orders one at a time.
- Exceptions use `adn_approval_core` and are linked to the affected quotation/order. The exception does not change the permanent credit limit.
- Credit-limit changes have a separate approval request and apply action.

## FSD rules

| Condition | Result |
|---|---|
| Exposure ≤ 80% | Normal under the approved FSD/TDD boundary |
| Exposure > 80% and ≤ 100% | Warning under the approved FSD/TDD boundary |
| Exposure > 100% | Hold + approval under the approved FSD/TDD boundary |
| Invoice overdue 1–30 calendar days | Warning + Finance review |
| Invoice overdue > 30 calendar days | Hold + Finance Manager approval |
| Finance-blocked customer | No order confirmation; no transaction exception bypass |
| Over-limit amount ≤ IDR 25,000,000 | Finance Manager |
| Over-limit amount > IDR 25,000,000 | Finance Manager + Managing Director |
| Credit-limit change | Finance Manager |
| Credit-limit increase threshold > IDR 100,000,000 | Finance Manager + Managing Director, subject to threshold-basis decision |

Thresholds are strict: exactly 80% is normal; exactly 100% is warning; exactly IDR 25,000,000 over limit routes to Finance Manager; exactly IDR 100,000,000 for the limit-change threshold remains Finance Manager.

**Boundary reconciliation required before activation:** the approved FSD/TDD classify exactly 80% as Normal and exactly 100% as Warning; the project-level credit rule describes Warning at 80% and Hold at 100%. Company settings therefore require Finance/Business to explicitly select the warning boundary (`above_80` or `at_80`) and hold boundary (`above_100` or `at_100`) before enabling credit control. The seeded behavior is not silently assumed.

## DEC-006 implementation gates

The approved TDD/RTM still marks DEC-006 open. The addon therefore ships with the company credit-control switch off and both approval policies inactive. Existing sales confirmation is not intercepted until Finance explicitly enables the company setting. Before enabling, configure:

1. `adn_credit_commitment_basis`: choose `Order Total Less Posted Invoice Lines` only after Finance approves the overlap resolver.
2. `adn_credit_trigger_point`: the current implementation supports Sales Order Confirmation only.
3. `adn_credit_warning_boundary` and `adn_credit_hold_boundary`: resolve the 80% and 100% boundary discrepancy between the project rule and approved FSD/TDD.
4. `adn_credit_exception_validity_start` and `adn_credit_exception_validity_hours`: the current implementation measures validity from request submission; set the Finance-approved duration.
5. `adn_credit_limit_threshold_basis`: Finance must decide whether the IDR 100,000,000 credit-limit-change threshold applies to the amount of the increase or the resulting limit.
6. Activate `CREDIT_EXCEPTION` and `CREDIT_LIMIT_CHANGE` policies only after their decisions and approver assignments are signed off.
7. A system administrator enables `Enable Customer Credit Control` for the company only after the preceding configuration and UAT sign-off. Company-level rollout settings are intentionally restricted to system administrators; Finance roles maintain customer credit profiles and execute the approval workflow.

### Commitment resolver

For each confirmed order, commitment is calculated as the order total (company-currency converted) less posted `out_invoice` product invoice lines linked to that order's sales lines. Draft invoices and customer credit notes are not subtracted. Line-level linkage avoids subtracting a grouped invoice's full amount from every linked sales order.

This is a deliberate, explicit resolver—not a claim that DEC-006 has been closed. Finance must validate down payments, global invoice discounts, manual invoices not linked to sales lines, rounding, and any local invoicing customizations before setting the company basis. If one posted invoice line is linked to multiple sales orders, evaluation fails closed rather than subtracting the same line from each order. The current quotation is included at its gross order total when it is being confirmed. Order commitments are converted at the company-local confirmation date and the conversion date is retained on the order to prevent later FX-rate drift.

## Security

- Sales users receive `Credit Exception Requester` through the standard Salesperson group and can submit requests for their own sales transactions.
- Finance Credit Managers maintain profiles, block/unblock customers, and apply approved limits.
- Finance Manager and Managing Director groups act on exception/limit approval steps.
- Detailed evaluation records and exposure values are restricted to Finance groups and company record rules.
- Credit status and evaluation audit fields are server-managed. A missing customer profile is treated as a zero credit limit; positive exposure therefore holds until Finance establishes an approved limit or grants a transaction-specific exception.
- Approval policies are inactive by default; do not activate before DEC-006 closure.

## Installation / upgrade

The adapter requires `adn_approval_core` 19.0.1.0.3 or later.

```bash
./odoo-bin -d <database> -u adn_approval_core --stop-after-init
./odoo-bin -d <database> -i adn_credit_control --stop-after-init
```

The standard `sales_team.group_sale_salesman` group implies Credit Exception Requester; verify group assignment for Sales users. Assign Finance Credit Manager and approver groups according to the approved role matrix.

## Tests

Included tests cover 80% / 100% boundaries, overdue rules, Finance block, zero credit limit, and combined hold reasons. Target-environment integration tests must additionally cover AR reconciliation, partial payments, multiple payment-term lines, partial invoice / grouped invoice overlap, multi-currency, concurrent confirmations, exception staleness/expiry, direct ORM state writes, imports/RPC, company isolation, and approval segregation of duties.

No Odoo runtime tests are claimed as executed in the build environment. Exception validity is measured from request submission time; this is the only implemented validity start point and must be accepted by Finance as part of DEC-006.
