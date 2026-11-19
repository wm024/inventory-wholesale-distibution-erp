# ADN Approval Core — Odoo 19

Reusable approval engine for the Inventory Wholesale Distribution project.

## Scope

- Policy and amount-tier rule configuration.
- Approval requests linked to standard Odoo source records by model and record ID.
- Approval steps, optional line-level approval items, and append-only audit events.
- Request submission, approval, rejection, cancellation, supersession, and release assertion.
- Company-aware policy selection and basic separation-of-duties enforcement.
- Policy, request, approval inbox, and audit user interfaces.

## Installation

1. Copy `adn_approval_core` into an addons directory included in `addons_path`.
2. Restart the Odoo 19 service.
3. Update the Apps list.
4. Install **ADN Approval Core**.
5. Assign the ADN Approval User, Approval Manager, and Approval Policy Administrator groups as appropriate.
6. Configure a policy, active rules, approver groups, effective dates, currency, and approval mode.

## Adapter contract

Transaction adapters must calculate policy inputs and a normalized snapshot from server-side source values. They submit using:

```python
request = self.env["adn.approval.request"].submit(
    policy_code="PURCHASE_ORDER",
    source_record=purchase_order,
    amount=purchase_order.amount_untaxed,
    snapshot={
        "currency": purchase_order.currency_id.name,
        "amount_untaxed": purchase_order.amount_untaxed,
        "lines": [
            {"product_id": line.product_id.id, "qty": line.product_qty,
             "price_unit": line.price_unit, "discount": line.discount}
            for line in purchase_order.order_line
        ],
    },
    reason="Business justification",
)
```

Immediately before the protected transaction action, the adapter must call:

```python
request.assert_released(purchase_order, "PURCHASE_ORDER", current_snapshot)
```

The adapter must also implement source fingerprint re-evaluation, source cancellation handling, and server-side action interception. The core deliberately does not confirm or post any business transaction.

## Important design boundaries

- The generic `source_model` + `source_res_id` pair is not a database foreign key. Adapters must validate source existence and access.
- Do not use `sudo()` to bypass approval authorization.
- Do not accept an actor user ID from a client; the engine uses `env.user`.
- Policy edits do not alter request snapshots or materialized approval steps.
- Audit events cannot be edited or deleted through normal ORM operations.
- Delegation is represented in the schema but is not enabled until a governed delegation policy is approved.
- Amount rules must be non-overlapping. The engine rejects ambiguous matching rules at submission.

## Validation status

This is an implementation package prepared from ADN-TDD-001. It has not been installed or executed against a real Odoo 19 database in this environment. Validate model fields, view syntax, method behavior, security, and test results against the exact target Odoo 19 build before promotion.
