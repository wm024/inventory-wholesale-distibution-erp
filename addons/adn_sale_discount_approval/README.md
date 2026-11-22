# ADN Sales Discount Approval

**Version:** 19.0.1.0.1  
**Platform:** Odoo 19 Enterprise  
**Depends on:** `sale_management`, `adn_approval_core`

## 1. Purpose

Implements the ADN per-sales-order-line discount approval adapter on standard Odoo `sale.order` and `sale.order.line`. It uses `adn_approval_core` for request routing, approval steps, decision history, and audit events. It does not create a parallel sales order or pricing ledger.

## 2. Approved FSD Tier Matrix

| Evaluated line discount | Required authority |
|---|---|
| 0%–5% | Sales Representative authority; no approval request |
| Above 5%–10% | Sales Supervisor |
| Above 10%–15% | Sales Manager |
| Above 15% | Sales Manager, then Managing Director |

The highest applicable line tier determines the approval route for the order. Every controlled line is retained as an `adn.approval.item`, with its own evaluated percentage, tier, reference price, reason, and source-line reference. The order cannot be confirmed until the request is approved.

Boundary behavior is strict and explicit: 5.00% does not require approval; 5.01% routes to Supervisor; 10.00% remains Supervisor; 10.01% routes to Manager; 15.00% remains Manager; above 15.00% routes to Manager and Managing Director.

## 3. DEC-002 Is a Go-Live Gate

The approved source documents explicitly leave DEC-002 open. The business must confirm:

- Discount reference price: pricelist unit price before discount, product list price, contract price, or another approved basis.
- Percentage rounding precision and rounding method.
- Whether multiple/cumulative discounts exist and how they are combined.
- Reapproval scope after a partial line amendment.

For that reason, the seeded `SO_DISCOUNT_APPROVAL` policy is **inactive**. It must not be activated until the Sales Manager resolves DEC-002 and configures these policy fields:

- `adn_discount_reference_basis`
- `adn_discount_rounding_digits`
- `adn_discount_rounding_method`
- `adn_discount_cumulative_mode`

Supported reference basis options are Sales Order Line Unit Price Before Discount, Product Sales Price/List Price, and Custom Resolver. Custom reference-price and cumulative-discount modes require a developer override of the corresponding resolver method. The standard cumulative mode uses Odoo's `sale.order.line.discount` field only. It explicitly blocks Odoo global-discount lines until a custom cumulative resolver is configured.

If no active policy exists, an order with an explicit non-zero Odoo line discount is blocked at confirmation and displays a configuration message. This is a fail-closed guard for explicit discounts; full evaluation of negotiated unit-price differences is only possible once the approved reference basis is configured. Do not treat the inactive seed policy as production-ready.

## 4. Workflow

1. Sales user prepares a quotation/order and enters the discount exception reason for every line above 5%.
2. The adapter resolves the active policy and calculates each line's effective unit price and discount percentage against the configured reference price.
3. The highest controlled tier selects the approval rule.
4. A single core approval request is created for the order, with line-level approval items for every controlled line.
5. Approvers review customer, product, reference price, effective price, discount percentage, reason, and order value.
6. The request becomes approved only after all routed approval steps are complete.
7. The server-side confirmation guard re-evaluates the source fingerprint and prevents confirmation while approval is missing, pending, rejected, or superseded.
8. Changes to customer, pricelist, terms, line product, quantity, UoM, unit price, discount, tax, description, or discount reason supersede a pending/approved request. A new submission is required.

## 5. Technical Design

### Standard models extended

- `sale.order`: approval request link, state, fingerprint, submit/open actions, confirmation guard.
- `sale.order.line`: reference price snapshot, evaluated discount percentage, tier, approval state/item, mandatory exception reason.
- `adn.approval.policy`: DEC-002 configuration fields.
- `adn.approval.rule`: percentage-based rule ranges and inclusive/exclusive operators.
- `adn.approval.request`: internal `_submit_with_rule` adapter API for non-monetary tier selection; public RPC `submit` remains amount-routed.

### Key controls

- Per-line discount evaluation.
- Highest-tier routing for mixed-tier orders.
- Mandatory reason for controlled lines.
- Self-approval prevention inherited from approval core.
- Manager + Managing Director sequential steps for discounts above 15%.
- Server-side guards on `action_confirm`, `_action_confirm`, and direct state writes to `sale`/`done`.
- Fingerprint-based amendment invalidation.
- Approval items and events retained as audit evidence.

## 6. Security Groups

- Sales Discount Approval Requester
- Sales Supervisor — Discount Approver
- Sales Manager — Discount Approver
- Managing Director — Discount Approver

Approver groups inherit the core Approval User group. Membership must be mapped to named business users during deployment. The ERP administrator does not receive business approval authority merely by being a technical administrator.

## 7. Installation

Install/upgrade the shared core before this adapter:

```bash
./odoo-bin -d <database> -u adn_approval_core --stop-after-init
./odoo-bin -d <database> -i adn_sale_discount_approval --stop-after-init
```

Then:
1. Assign the Sales requester and approver groups.
2. Resolve DEC-002 with the Sales Manager.
3. Open Approval Policies and edit `SO_DISCOUNT_APPROVAL`.
4. Select reference basis, rounding precision/method, and cumulative discount treatment.
5. Review percentage rules and approver group membership.
6. Increment policy version, activate the policy, and execute the complete boundary/negative/regression test set.

## 8. Tests

Included automated tests cover the six FSD boundary values and the DEC-002 activation gate. The deployment test plan must additionally cover mixed-tier multi-line orders, missing/zero reference price, reason requirement, currency conversion for list price, custom resolver, amendment after approval, rejected request resubmission, self-approval, unauthorized approval, and confirmation via UI/import/RPC/API.

Run in the target Odoo 19 environment:

```bash
./odoo-bin -d <test_database> -i adn_sale_discount_approval --test-enable --stop-after-init
```

Static checks are not a substitute for Odoo runtime tests. Verify the exact Odoo 19 build and installed Sales modules before production deployment.

## 9. Known Limitations / Decisions

- DEC-002 remains unresolved; seeded policy is inactive.
- Custom contract-price logic requires an approved resolver implementation.
- Custom stacked/cumulative discount logic requires an approved resolver implementation.
- The base adapter treats all controlled lines as covered by the highest applicable order-level tier, consistent with the FSD's highest-tier rule. If the business instead requires independent per-line approval chains, that is a scope/design change.
- Delegation and approver substitution are not implemented in the shared approval core baseline.
