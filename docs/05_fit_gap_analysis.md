# FIT-GAP ANALYSIS
## Odoo 19 Enterprise ERP Implementation — Advanced Wholesale Distribution & Supply Chain

**Company:** PT Arunika Distribusi Nusantara  
**Project ID:** ADN-ERP-2026-001  
**Document ID:** ADN-FGA-001  
**Version:** 1.0  
**Date:** 18 November 2026  
**Status:** Approved for Technical Design
**ERP Platform:** Odoo 19 Enterprise  
**Deployment:** On-Premise | Ubuntu Linux | PostgreSQL  
**Currency:** Indonesian Rupiah (IDR)  
**Primary Source:** Functional Specification Document ADN-FSD-001 v1.0  
**Related Baselines:** BRD ADN-BRD-001 v1.1; SOW ADN-SOW-001 v1.0; Business Process Mapping ADN-BPM-001 v1.0  
**Classification:** Portfolio / Fictional Business Case

> **Portfolio Disclaimer**  
> PT Arunika Distribusi Nusantara, its stakeholders, policies, thresholds, transaction values, and implementation scenario are fictional. This document is a preliminary design assessment, not evidence of an installed Odoo environment, completed product demonstration, stakeholder approval, or production implementation. All Odoo capabilities, edition entitlements, localization behavior, and technical assumptions must be verified in the target Odoo 19 database before final design approval.

---

# 1. Executive Summary

## 1.1 Purpose

This Fit-Gap Analysis (FGA) evaluates the functional requirements documented in ADN-FSD-001 v1.0 against the intended capabilities of Odoo 19 Enterprise. It identifies where a requirement is expected to be met by standard Odoo functionality, where configuration is required, where a controlled manual procedure may be sufficient, and where a customization or integration may be necessary.

The analysis is intended to support:
- Functional validation workshops.
- Standard-versus-customization decisions.
- Scope and effort estimation.
- Customization prioritization.
- Technical Design Document (TDD) preparation.
- Test planning and requirements traceability.
- Formal decisions on unresolved functional policies.

## 1.2 Overall Assessment

The proposed solution is broadly aligned with Odoo's standard ERP application areas: Contacts, CRM, Sales, Purchase, Inventory, Barcode, Quality, Accounting, and reporting. Core transaction lifecycles such as quotation-to-order, purchase-to-receipt, stock movements, invoicing, payments, and reconciliation are expected to be addressed primarily through standard functionality and configuration.

The main areas likely to require controlled customization are business-specific approval controls and derived management logic, particularly:
- Multi-level purchase order approval by value, including re-approval after amendment.
- Sales discount approval by order line.
- Customer credit exposure calculation and transaction-specific credit holds.
- Inventory adjustment approval by absolute valuation difference.
- Refund approval and execution lock.
- Vendor performance scorecards and weighted KPI calculation.
- Selected dashboard measures, delivery discrepancy tracking, and shelf-life enforcement where standard configuration is insufficient.

This is a preliminary fit-gap conclusion. No feature is classified as definitively available in the target database until it has been demonstrated and tested in the actual Odoo 19 environment.

## 1.3 Key Recommendations

1. Adopt standard Odoo transaction objects as the system of record; do not create parallel sales, purchase, stock, or accounting ledgers.
2. Configure standard features first: warehouses, routes, reordering rules, tracking, removal strategies, quality control points, product categories, journals, taxes, and user groups.
3. Implement one reusable approval framework for PO, discount, credit exception, inventory adjustment, and refund workflows where technically and functionally appropriate.
4. Keep approval policy values in controlled configuration rather than hard-coded business logic.
5. Treat vendor scorecard and consolidated KPI requirements as governed reporting features with documented formulas, date rules, refresh logs, and drill-down.
6. Confirm Indonesian localization, tax configuration, accounting mappings, and statutory reporting with qualified Finance/tax reviewers before any real deployment.
7. Resolve the open decisions in Section 13 before finalizing the TDD and development estimates.

## 1.4 Fit-Gap Status Summary

| Classification | Meaning | Preliminary Assessment |
|---|---|---|
| **FIT** | Expected to be met by standard Odoo behavior with no material change | Core CRM, sales, purchase, stock movements, lots/serials, invoices, payments, reconciliation |
| **CONFIGURATION** | Standard Odoo capability requiring setup, master data, routes, rules, security, or reporting configuration | Warehouses, UoM, FEFO, FIFO/AVCO, automated valuation, quality checks, replenishment, access groups |
| **PARTIAL FIT** | Standard capability covers part of the requirement; additional controls, fields, reporting, or workflow may be needed | Three-way matching, expiry restrictions, delivery KPI/POD, quality sampling, stock aging |
| **CUSTOMIZATION** | Requirement is expected to need an approved custom addon or extension | Approval matrices, credit exposure/holds, vendor scorecard, selected custom dashboards |
| **MANUAL / PROCEDURAL** | A controlled human activity is appropriate and should be recorded in Odoo | Physical inspection, supplier negotiation, discrepancy investigation, approval evidence review |
| **INTEGRATION / TBD** | Depends on an external system, licensed capability, or unresolved technical/business decision | External carrier/bank interfaces (currently out of scope), scheduled jobs, optional system exchanges |
| **OPEN DECISION** | Business policy or design rule is not sufficiently defined for implementation | Listed in Section 13 |

---

# 2. Document Control

## 2.1 Revision History

| Version | Date | Description | Author |
|---|---|---|---|
| 1.0 | 18-Nov-2026 | Initial fit-gap assessment based on ADN-FSD-001 v1.0 | ERP Business Analyst |

## 2.2 Review and Approval

| Role | Review Responsibility | Status |
|---|---|---|
| Project Sponsor / Managing Director | Scope, policy, executive approval boundaries | Pending |
| Operations Manager | Inventory, warehouse, quality, logistics, adjustment approvals | Pending |
| Procurement Manager | Purchase workflow, vendor evaluation, PO approval | Pending |
| Sales Manager | CRM, sales, pricing, discount approval | Pending |
| Finance Manager | Credit, accounting, costing, tax assumptions, refund and landed cost | Pending |
| ERP Project Manager | Scope baseline, dependencies, decision log | Pending |
| Odoo Functional Lead | Standard feature validation and configuration feasibility | Pending |
| Odoo Technical Lead | Customization feasibility, architecture, maintainability | Pending |

## 2.3 Source Documents

| Document | Reference | Version | Usage |
|---|---|---:|---|
| Business Requirements Document | ADN-BRD-001 | 1.1 | Business rules, priorities, policies, expected outcomes |
| Scope of Work | ADN-SOW-001 | 1.0 | In-scope work packages, exclusions, deliverables, acceptance |
| Business Process Mapping | ADN-BPM-001 | 1.0 | AS-IS / TO-BE process context |
| Functional Specification Document | ADN-FSD-001 | 1.0 | Functional requirements and intended Odoo behavior |
| Fit-Gap Analysis | ADN-FGA-001 | 1.0 | Standard/configuration/customization decision baseline |

## 2.4 Assessment Limitations

- The assessment is based on the written FSD, not a live Odoo database or product demonstration.
- Odoo 19 Enterprise application availability, licensing, localization, installed modules, and exact user-interface behavior have not been independently verified.
- A standard feature name does not prove that the feature satisfies every ADN business rule.
- A custom classification is a candidate pending proof that configuration or standard controls cannot satisfy the requirement.
- No external integrations are assumed unless explicitly approved through scope/change control.
- Tax rates and tax treatments in the source requirements are illustrative portfolio assumptions, not tax advice.

---

# 3. Business and Solution Context

## 3.1 Operating Model

The target business is a fictional Indonesian B2B wholesale distributor of FMCG, household products, and consumer goods. The FSD defines one legal entity, IDR as primary currency, and three warehouses:

| Warehouse | Code | Primary Role |
|---|---|---|
| Jakarta Central Warehouse | WH-JKT | Main supplier/import receiving and central allocation |
| Bandung Regional Warehouse | WH-BDG | West Java fulfillment and replenishment |
| Surabaya Regional Warehouse | WH-SBY | East Java fulfillment and regional inventory control |

Planning data includes 500 SKUs, 250 customers, 40 vendors, 20 user-role staging records, and 30+ internal locations.

## 3.2 Odoo Application Areas in the Assessment

| Business Capability | Odoo Application / Feature | Fit-Gap Focus |
|---|---|---|
| Master Data | Contacts, Products, UoM, Product Categories | Uniqueness, attributes, ownership, imports |
| CRM | CRM | Lead, opportunity, activity, quotation conversion |
| Sales | Sales | Pricelists, discounts, order confirmation, delivery creation |
| Procurement | Purchase | RFQ, vendor comparison, PO lifecycle, approvals |
| Inventory | Inventory | Warehouses, locations, routes, lots, serials, reservations, valuation |
| Warehouse Execution | Barcode, Inventory | Scanning, receiving, picking, packing, dispatch |
| Quality | Quality, Inventory | Control points, checks, sampling, disposition |
| Finance | Accounting / Invoicing | AR/AP, invoices, credit notes, payment, reconciliation |
| Landed Costs | Inventory Landed Costs | Cost lines, allocation, valuation impact |
| Documents / Audit | Chatter, attachments, Documents where licensed | Evidence and source-document linkage |
| Reporting | Standard reports, list/pivot/graph views, approved custom reporting | KPI definitions, data lineage, refresh |
| Access Control | Users, Groups, ACLs, Record Rules | Least privilege and segregation of duties |
| Custom Workflow | ADN-approved addons | Approval engine, credit controls, scorecards |

## 3.3 Design Principles

- Standard Odoo remains the transaction system of record.
- Configuration is preferred over code where it meets the requirement.
- Customization is justified by a documented functional gap and approved business value.
- Business policy thresholds must be maintained as controlled parameters where feasible.
- Custom code must not bypass standard stock, accounting, or document validation.
- Approval decisions must be auditable and bound to the affected source transaction.
- The same business rule must produce consistent results in UI, imports, RPC/API calls, and automated jobs.
- All custom features require negative tests, boundary tests, access tests, and regression tests.

---

# 4. Fit-Gap Assessment Methodology

## 4.1 Assessment Steps

1. Extract each functional requirement and business rule from ADN-FSD-001.
2. Identify the Odoo application/object/process expected to support it.
3. Assess standard capability at a conceptual level.
4. Identify required configuration, master data, security, or procedural controls.
5. Identify any remaining gap and the smallest viable extension.
6. Define the validation evidence required in the target environment.
7. Assign an owner, priority, dependency, and decision status.
8. Baseline the approved outcome before TDD and build.

## 4.2 Classification Definitions

| Code | Classification | Decision Rule |
|---|---|---|
| FIT | Standard fit | Standard Odoo behavior satisfies the requirement after ordinary setup |
| CFG | Configuration fit | Standard feature satisfies the requirement after configuration |
| P-FIT | Partial fit | Standard capability covers only part of the functional behavior |
| CUS | Customization required | Confirmed policy/logic cannot be achieved acceptably through standard setup |
| MAN | Manual / procedural | Human judgment or physical action is required; Odoo records the outcome |
| INT | Integration | Approved exchange with an external system is required |
| TBD | To be determined | Evidence or business decision is insufficient |

## 4.3 Fit-Gap Decision Rules

- Do not select CUS merely because a custom implementation is easier to describe.
- Do not select FIT merely because Odoo has a similarly named application or button.
- A requirement involving a hard control (e.g., block confirmation) must be tested at the server/business-logic level, not only by hiding a button.
- If a workflow needs approval, verify approver routing, self-approval prevention, delegated authority, amendment behavior, audit history, and execution lock.
- If a KPI is required, verify its formula, data source, date basis, inclusion/exclusion rules, rounding, refresh, and drill-down.
- If a requirement depends on a licensed app or optional module, record the entitlement dependency.
- Any policy ambiguity remains an OPEN DECISION; the analyst must not invent a business rule.

## 4.4 Evidence Levels

| Evidence Level | Description | Status Implication |
|---|---|---|
| E0 — FSD desk assessment | Inferred from written requirements and general Odoo application mapping | Preliminary only |
| E1 — Environment inspection | Installed apps, settings, edition, localization, and relevant models inspected | Stronger assessment |
| E2 — Configuration prototype | Requirement configured in a representative database | Demonstrated candidate |
| E3 — Functional test | Positive, negative, boundary, and role tests passed | Validated fit/gap |
| E4 — Business sign-off | Process owner accepts behavior and evidence | Approved baseline |

All assessments in this document begin at **E0** unless otherwise stated. No E1–E4 result is claimed.

---

# 5. Fit-Gap Register — Master Summary

| Gap ID | Domain | FSD Reference | Requirement / Capability | Preliminary Fit | Proposed Treatment | Priority | Evidence / Decision Required |
|---|---|---|---|---|---|---|---|
| GAP-MD-001 | Master Data | FSD-MD-001–010 | Products, customers, vendors, UoM, warehouses, locations, tracking | CFG | Configure standard master records, groups, import templates, validation | Must | E1/E2 import and uniqueness tests |
| GAP-CRM-001 | CRM | FSD-CRM-001–007 | Leads, opportunities, activities, conversion | FIT/CFG | Standard CRM pipeline and activity setup | Should | Demonstrate lead conversion and quotation linkage |
| GAP-SAL-001 | Sales | FSD-SAL-* | Quotation, sales order, pricelist, delivery and invoice lifecycle | FIT/CFG | Standard Sales setup and invoicing policy | Must | E2 O2C walkthrough |
| GAP-SAL-002 | Sales Discount | FSD-SAL-*; FSD-SEC | Discount approval per order line | CUS candidate | Custom approval routing and confirmation lock if standard setup cannot enforce policy | Must | Confirm discount basis, rounding, multiple discounts, amendment rules |
| GAP-CRD-001 | Credit | FSD-CRD-* | Exposure, warning, hold, exception release | CUS candidate | Credit exposure service and order-level approval extension | Must | Confirm exposure formula and trigger |
| GAP-PUR-001 | Procurement | FSD-PUR-001–005 | Replenishment demand, request, RFQ, vendor comparison | CFG/P-FIT | Configure reordering, purchase agreements/alternatives subject to app validation | Must | Verify requisition capability and comparison workflow |
| GAP-PUR-002 | PO Approval | FSD-PUR-006–008 | Multi-level PO approval and re-approval after amendment | CUS candidate | Approval engine with tier calculation and server-side confirmation lock | Must | Validate authority, substitution, split-order monitoring |
| GAP-PUR-003 | Three-Way Match | FSD-PUR-011; FSD-ACC-009 | PO/accepted receipt/vendor bill matching, 2% quantity and 1% price tolerances | P-FIT | Configure standard bill controls; extend variance calculation/blocking if required | Must | Validate matching basis, UoM, taxes, discounts |
| GAP-SUP-001 | Replenishment | FSD-SUP | Warehouse min/max, forecast, internal vs external supply | CFG | Configure warehouse-specific rules and routes | Must | Validate forecast semantics and source selection |
| GAP-SUP-002 | Inter-Warehouse | FSD-SUP | Transfer request, transit, partial receipt, lot continuity | CFG/P-FIT | Configure routes/operation types/transit locations; custom approval only if policy demands | Must | Confirm transfer authority and transit accounting |
| GAP-INV-001 | Inventory | FSD-INV-001–008, 011–013 | Stock, warehouses, locations, lots/serials, expiry, FEFO, reservation | CFG | Configure tracking, removal strategies, locations, reservation | Must | Test multi-warehouse FEFO and expiry behavior |
| GAP-INV-002 | Shelf-Life Enforcement | FSD-INV-006–007 | 90-day minimum at dispatch and expiry-based restrictions | P-FIT/CUS candidate | Configure expiry alerts/removal rules; custom customer/order shelf-life validation if needed | Must | Define override authority and exact date logic |
| GAP-INV-003 | Costing | FSD-INV-008; FSD-ACC-007–008 | FIFO/AVCO by category, automated valuation | CFG | Configure categories, valuation accounts, journals; controlled migration | Must | Finance-led Odoo 19 accounting prototype |
| GAP-INV-004 | Adjustment Approval | FSD-INV-009; FSD-SEC | Approval by absolute valuation difference | CUS candidate | Approval extension with valuation basis and validation lock | Must | Define aggregation/rounding and multi-product adjustment treatment |
| GAP-INV-005 | Cycle Count / Aging | FSD-INV-010, 014–015 | Count scheduling, stock aging and valuation reports | CFG/P-FIT | Standard count/report configuration; custom aging only if source report insufficient | Should | Agree aging date basis and report reconciliation |
| GAP-WH-001 | Warehouse Execution | FSD-WH | Receiving, putaway, picking, packing, dispatch | FIT/CFG | Configure warehouse steps, putaway, reservation, Barcode if licensed | Must | Test all three warehouse flows and devices |
| GAP-QUA-001 | Quality | FSD-QUA | Incoming/outgoing inspections and dispositions | CFG/P-FIT | Configure control points and checks; add controlled checklist fields if required | Must | Confirm sampling and disposition authority |
| GAP-QUA-002 | Sampling | FSD-QUA-003 | Sample quantity rules and critical defect hold | P-FIT/CUS candidate | Manual sampling initially; custom sample calculation only if operationally required | Should | Approve sample rules and handling of mixed lots |
| GAP-LOG-001 | Logistics | FSD-LOG-001–004 | Delivery dates, dispatch status, POD | CFG/P-FIT | Use delivery transfers, scheduled/validation dates, attachments; add fields if needed | Must | Confirm planned vs actual delivery date semantics |
| GAP-LOG-002 | Delivery KPI / Discrepancy | FSD-LOG-005–006 | Discrepancy records and delivery KPIs | P-FIT/CUS candidate | Add structured discrepancy fields and report calculations if standard views insufficient | Should | Define promised date, partial-delivery KPI treatment |
| GAP-RET-001 | Returns | FSD-RET | Customer and supplier returns, quarantine, disposition | FIT/CFG | Standard return transfers/credit notes/vendor credits with configured locations | Must | E2 return walkthrough |
| GAP-RET-002 | Refund Approval | FSD-RET; FSD-SEC | Refund value tiers and execution lock | CUS candidate | Approval workflow linked to credit note/refund execution | Must | Confirm gross/net basis and refund payment path |
| GAP-ACC-001 | Accounting | FSD-ACC-001–008, 010 | Invoices, bills, AR/AP, payments, reconciliation, statements | FIT/CFG | Configure chart, journals, payment terms, accounts, reports | Must | Finance sign-off and reconciliation tests |
| GAP-ACC-002 | Indonesian Tax | FSD-ACC-007 | Indonesian localization and tax mapping | TBD/CFG | Inspect localization availability and configure only after professional review | Must | Confirm localization version and current tax treatment |
| GAP-LC-001 | Landed Cost | FSD-LC | Freight, insurance, customs, handling allocation | CFG/P-FIT | Configure landed cost products/methods and validate valuation | Must | Test cost methods, already-sold quantities, closed periods |
| GAP-VPM-001 | Vendor Scorecard | FSD-VPM | Monthly/rolling KPIs, weighted score, insufficient-data state | CUS | Custom reporting model/job or governed report layer | Must | Confirm period cut-off, due quantity and reference price |
| GAP-RPT-001 | Management Dashboards | FSD-RPT | Inventory, sales, procurement, warehouse, finance dashboards | P-FIT/CUS candidate | Standard list/pivot/graph first; custom consolidated dashboards selectively | Should | Validate KPI formulas, filters, security, refresh |
| GAP-SEC-001 | Security / SoD | FSD-SEC | Role access, self-approval prevention, auditability | CFG/CUS | Groups/ACLs/record rules plus custom approval permissions | Must | Role matrix and negative access tests |
| GAP-MIG-001 | Data Migration | FSD-MIG | Master data and opening balances | CFG/MAN | Standard import templates, staging validation, controlled reconciliation | Must | Confirm cut-off, opening data, migration ownership |
| GAP-NFR-001 | Non-Functional | FSD Section 9 | Performance, backup, restore, security, scalability | TBD/CFG | Infrastructure and operational design; performance/restore tests | Must | Confirm hardware, concurrency, RPO/RTO, backup policy |

---

# 6. Detailed Fit-Gap Assessment by Functional Domain

## 6.1 Master Data Management

**FSD references:** FSD-MD-001 to FSD-MD-010  
**Odoo areas:** Contacts, Products, UoM, Product Categories, Inventory, Users/Groups  
**Preliminary result:** **CFG — Expected fit through standard records and controlled import**

### Standard capability expected to fit
- Product, customer, and vendor records.
- Product categories, internal references, barcodes, UoM and purchase UoM.
- Multiple contact addresses and partner roles.
- Warehouses and hierarchical stock locations.
- Lot/serial tracking and expiration configuration.
- User groups and role assignment.

### Configuration required
- Unique coding conventions and mandatory fields.
- Product category hierarchy and valuation policy.
- Customer/vendor payment terms and tax placeholders.
- Three warehouse structures and location naming conventions.
- Product tracking and expiration settings.
- Import templates, dependency sequence, and user groups.

### Potential gaps
- Enforced approval for master data creation/amendment is not fully specified as a standard workflow in the FSD. If dual control is mandatory, confirm whether groups and record rules suffice or whether an approval extension is required.
- Cross-object duplicate checks for external identifiers may need import validation or a small extension depending on the uniqueness rule.
- Credit attributes may require custom fields and logic; assessed separately under GAP-CRD-001.

### Recommendation
Use standard Odoo master objects. Create controlled templates and a staging validation process. Do not create separate custom product/customer/vendor ledgers.

### Validation scenarios
1. Import duplicate product/customer/vendor codes.
2. Import product with missing category or UoM.
3. Import tracked opening stock with missing lot/expiry.
4. Verify archive behavior for records referenced by transactions.
5. Verify users receive only assigned groups.

**Decision owner:** Data Owner / ERP Manager  
**Priority:** Must

---

## 6.2 CRM and Lead Management

**FSD references:** FSD-CRM-001 to FSD-CRM-007  
**Odoo areas:** CRM, Sales, Contacts  
**Preliminary result:** **FIT / CFG**

### Standard capability expected to fit
- Lead and opportunity pipeline.
- Sales team and salesperson assignment.
- Activity scheduling, calls, meetings, and follow-up.
- Won/lost stages and lost reasons.
- Conversion from opportunity to quotation.

### Configuration required
- Pipeline stages and qualification criteria.
- Sales teams, assignment rules, lost reasons, and activity types.
- Customer segmentation fields only where required by the approved BRD.

### Potential gaps
- Additional segmentation or management reporting may need fields or report configuration.
- Automated lead sourcing from external platforms is not assumed; such integration is outside the current baseline unless approved.

### Recommendation
Use standard CRM first. Do not customize the opportunity lifecycle unless a demonstrated requirement cannot be met through configuration.

### Validation scenarios
- Create lead, qualify, convert to opportunity, record activity, create quotation, and confirm traceability.
- Validate access to team-owned opportunities.
- Validate won/lost reporting.

**Decision owner:** Sales Manager  
**Priority:** Should

---

## 6.3 Sales, Pricing, and Order-to-Cash

**FSD references:** FSD-SAL; E2E-002  
**Odoo areas:** Sales, Contacts, Inventory, Accounting  
**Preliminary result:** **FIT / CFG for core O2C; CUS candidate for discount approval**

### Standard capability expected to fit
- Quotations and sales orders.
- Customer-specific and volume pricelists, subject to correct configuration.
- Delivery creation from confirmed sales orders.
- Invoicing policy and customer invoice generation.
- Credit notes and payment/reconciliation through Accounting.

### Configuration required
- Pricelist rules, product/customer assignment, payment terms, sales teams, warehouses, routes, invoicing policy, and taxes.
- Delivery reservation and backorder behavior.
- Sales user groups and document access.

### Gap: discount approval per order line
The FSD defines the following discount tiers:

| Discount per Order Line | Required Authority |
|---|---|
| 0%–5% | Sales Representative |
| Above 5%–10% | Sales Supervisor |
| Above 10%–15% | Sales Manager |
| Above 15% | Sales Manager and Managing Director |

A standard discount field does not by itself prove that the required approval routing, confirmation lock, audit history, and re-approval after amendment are enforced.

**Proposed treatment:** CUS candidate. Add approval state and tier calculation per sales order line, or a transaction-level approval object that identifies every line requiring approval. Prevent order confirmation while any required approval is pending. Re-evaluate when quantity, unit price, discount, pricelist, or other policy-defined value changes.

### Validation scenarios
- Apply discounts at 5%, 5.01%, 10%, 10.01%, 15%, and 15.01%.
- Attempt confirmation while approval is pending.
- Amend an approved line and verify re-approval.
- Test multi-line orders with different approval tiers.
- Confirm posted credit notes reduce net sales reporting.

**Open decisions:** Discount reference price, rounding, cumulative discounts, line vs order aggregation, amendment behavior.  
**Decision owner:** Sales Manager  
**Priority:** Must for discount control; core O2C Must

---

## 6.4 Credit Management

**FSD references:** FSD-CRD; E2E-005  
**Odoo areas:** Sales, Accounting, Contacts  
**Preliminary result:** **CUS candidate**

### Required business behavior
- Calculate customer credit exposure.
- Provide warning when exposure exceeds 80% of approved credit limit.
- Apply hold when exposure exceeds 100%.
- Apply credit hold when an invoice is more than 30 days overdue.
- Route exceptions based on over-limit amount and overdue status.
- Recalculate exposure before releasing an order.

### Standard capability expected to contribute
- Customer receivable balances and aging.
- Payment terms and accounting status.
- Sales order values and customer master data.
- Standard accounting reports for receivables.

### Gap
The FSD's exposure logic includes posted AR and open confirmed uninvoiced orders, with a requirement to avoid double counting once invoiced. The exact trigger and exception workflow are business-specific and require explicit calculation and enforcement.

### Proposed treatment
Implement a controlled credit exposure calculation and order hold extension if environment validation confirms standard features do not meet the exact rule. The calculation must:
1. Read posted outstanding receivables.
2. Include eligible confirmed uninvoiced sales orders.
3. Exclude/correctly offset amounts already represented in posted AR.
4. Apply the approved credit limit.
5. Identify overdue invoices over 30 days.
6. Recalculate at the confirmation/release point.
7. Record the affected order, approver, reason, decision, and expiry/validity of exception.

### Approval policy from FSD
- Over limit by up to IDR 25,000,000: Finance Manager.
- Over limit by more than IDR 25,000,000: Finance Manager and Managing Director.
- Overdue more than 30 days: Finance Manager.
- Credit limit change: Finance Manager.
- Increase above IDR 100,000,000: Finance Manager and Managing Director.

### Validation scenarios
- Exposure at 80%, above 80% through 100%, and above 100%.
- Overdue invoice exactly 30 days vs more than 30 days.
- Invoicing an order already included in exposure.
- Concurrent orders submitted against the same remaining credit.
- Exception approval and re-evaluation before release.

**Open decisions:** Exposure formula, order/invoice overlap, trigger point, exception expiry, concurrent order handling.  
**Decision owner:** Finance Manager  
**Priority:** Must

---

## 6.5 Procurement and Procure-to-Pay

**FSD references:** FSD-PUR-001 to FSD-PUR-012; E2E-001  
**Odoo areas:** Purchase, Inventory, Quality, Accounting  
**Preliminary result:** **CFG / PARTIAL FIT; CUS candidate for PO approval and possibly three-way matching**

### Standard capability expected to fit
- RFQ and purchase order lifecycle.
- Vendor product prices and lead-time information.
- Purchase-linked incoming receipts.
- Partial receipts and backorders.
- Vendor bills, payments, and reconciliation.
- Quality checks linked to receipt operations, subject to configuration.

### Configuration / validation required
- Replenishment rules and procurement routes.
- Purchase agreement or internal purchase request approach.
- Alternative RFQ/vendor comparison capability and its availability in the target environment.
- Vendor lead times and product/vendor data.
- Bill control policy and three-way matching behavior.

### Gap: PO approval
FSD approval tiers use untaxed PO value after line discounts:

| PO Value | Approver |
|---|---|
| IDR 0–10,000,000 | Procurement Supervisor |
| Above IDR 10,000,000–50,000,000 | Procurement Manager |
| Above IDR 50,000,000–150,000,000 | Operations Manager |
| Above IDR 150,000,000 | Managing Director |

**Proposed treatment:** CUS candidate for tier calculation, approval assignment, self-approval prevention, server-side PO confirmation lock, re-evaluation after value changes, and retained history.

### Gap: three-way matching
FSD tolerances:
- Quantity variance: maximum 2%.
- Price variance: maximum 1%.

Standard bill controls may cover some matching scenarios, but the exact line-level calculation and tolerances must be demonstrated. If the target behavior cannot be achieved through configuration, implement a variance exception layer and posting/payment control.

### Validation scenarios
- Test each PO threshold and exact boundary.
- Change an approved PO so it enters a higher tier.
- Attempt self-approval.
- Receive partially and bill partially.
- Test quantity variance at 2% and above 2%.
- Test price variance at 1% and above 1%.
- Test UoM conversion, taxes, discounts, freight, and landed cost basis.

**Open decisions:** Requisition method, vendor comparison feature, split-order detection criteria, tolerance basis, tax/UoM handling.  
**Decision owner:** Procurement Manager / Finance Manager  
**Priority:** Must

---

## 6.6 Replenishment and Inter-Warehouse Supply

**FSD references:** FSD-SUP; E2E-003  
**Odoo area:** Inventory  
**Preliminary result:** **CFG; partial fit for transfer approval**

### Standard capability expected to fit
- Reordering rules by product and warehouse/location.
- Forecasted stock and procurement routes.
- Internal transfers and multi-step routes.
- Partial transfer processing and stock movement traceability.

### Configuration required
- Minimum/maximum quantities, safety stock assumptions, and lead times.
- Warehouse-specific routes and source/destination locations.
- Transit locations and operation types.
- Lot/serial preservation and reservation rules.

### Potential gap
The FSD describes a transfer request and approval step where required by policy. The actual transfer approval authority is not fully defined. If mandatory approval cannot be achieved with standard access/configuration, use the shared approval framework.

### Recommendation
Configure standard replenishment and routes first. Use a transit location so destination stock is not available before receipt validation. Do not assume a custom transfer approval is required until the authority policy is approved.

### Validation scenarios
- Independent min/max rules per warehouse.
- Internal source selected when available; external procurement when appropriate.
- Partial dispatch and partial destination receipt.
- Lot/serial identity preserved in transit.
- Stock not available at destination before receipt validation.

**Decision owner:** Operations Manager  
**Priority:** Must

---

## 6.7 Inventory, Lot/Serial, Expiration, FEFO, and Costing

**FSD references:** FSD-INV-001 to FSD-INV-015  
**Odoo areas:** Inventory, Accounting  
**Preliminary result:** **CFG for core inventory; PARTIAL FIT for shelf-life enforcement, aging, and approval controls**

### Standard capability expected to fit after configuration
- Real-time stock balances and stock movement history.
- Multiple warehouses and hierarchical locations.
- Lot and serial tracking.
- Expiration date management.
- Removal strategies, including FEFO where supported by the configured product/location flow.
- Stock reservation and inventory valuation.
- FIFO/AVCO category costing and automated valuation, subject to target database validation.

### Configuration required
- Product tracking policy.
- Expiration dates and alert settings.
- FEFO removal strategy by eligible location/product.
- Quality, quarantine, damaged, and returns locations.
- Product category costing and valuation accounts.
- Cycle count frequency and roles.

### Gap: customer minimum shelf life
The FSD requires at least 90 days remaining shelf life at dispatch for designated products unless the customer contract is stricter. Standard expiry dates and FEFO do not automatically prove that a customer-specific minimum shelf-life rule is enforced at order allocation or delivery validation.

**Proposed treatment:** Configure standard expiration/removal rules first. If a customer/order-specific shelf-life check cannot be achieved through standard configuration, implement a validation that checks lot expiry against dispatch date and the applicable customer/product rule. Define a controlled override process.

### Gap: inventory adjustment approval
Approval is based on absolute valuation difference, not sales price:

| Absolute Difference Value | Approver |
|---|---|
| Up to IDR 1,000,000 | Warehouse Supervisor |
| Above IDR 1,000,000–10,000,000 | Warehouse Manager |
| Above IDR 10,000,000–50,000,000 | Operations Manager and Finance Manager |
| Above IDR 50,000,000 | Managing Director and Finance Manager |

A standard stock count does not by itself establish this value-tier approval and validation lock. Custom approval is required for the value-tier gate. DEC-003 was confirmed on 2026-11-22: calculate each changed adjustment line using inventory valuation cost, round each line using company currency precision, sum absolute line values without offsetting gains and losses, group by company + warehouse and accounting date, snapshot at submission and revalidate before release, and require parallel approval from every listed role. The existing value tiers remain unchanged.

### Costing policy
- CAT-001 Food & Beverage: FIFO, automated valuation.
- CAT-002 Household Cleaning: AVCO, automated valuation.
- CAT-003 Personal Care: FIFO, automated valuation.
- CAT-004 Kitchen Supplies: AVCO, automated valuation.
- CAT-005 Consumer Goods: AVCO, automated valuation.

The target Odoo 19 configuration must be tested for category costing, automated valuation, account mapping, landed cost effects, and opening stock reconciliation.

### Validation scenarios
- FEFO chooses earliest eligible expiry, not an expired/ineligible lot.
- Lot/serial identity preserved across receipt, transfer, delivery, and return.
- Shelf-life boundary at 90 days and customer override.
- Adjustment thresholds, aggregation, rounding, and self-approval.
- FIFO/AVCO valuation and GL reconciliation by category.
- Costing changes are restricted and subject to Finance approval.

**Open decisions:** Adjustment aggregation basis, valuation timing, shelf-life override authority, aging date basis, costing migration.  
**Decision owner:** Operations Manager / Finance Manager  
**Priority:** Must

---

## 6.8 Receiving, Putaway, Picking, Packing, and Dispatch

**FSD references:** FSD-WH; BPM-008 and BPM-009  
**Odoo areas:** Inventory, Barcode, Quality  
**Preliminary result:** **FIT / CFG**

### Standard capability expected to fit
- Purchase-linked receipts.
- Partial receipts and backorders.
- Putaway rules and multi-location stock.
- Delivery orders, reservation, picking, and backorders.
- Barcode scanning where app/device entitlements permit.

### Configuration required
- Three warehouse operation flows.
- Input, Quality, Stock zones, Packing, Output, Damaged, and Returns locations.
- Putaway and removal strategies.
- Reservation timing and partial delivery policy.
- User access by warehouse and operation.

### Potential gaps
- Mandatory dispatch checks and custom validations may need an extension if standard quality integration does not block validation for the exact scenarios.
- Barcode functionality depends on application entitlement, supported devices, and operational network design.

### Recommendation
Use standard multi-step warehouse operations. Validate the exact operational route at each warehouse before adding code.

### Validation scenarios
- Receipt-to-quality-to-putaway.
- Sales reservation-to-pick-to-pack-to-dispatch.
- Partial receipt and delivery.
- Quality-pending stock excluded from available stock.
- Barcode scan validation on actual target devices.

**Decision owner:** Operations Manager  
**Priority:** Must

---

## 6.9 Quality Management

**FSD references:** FSD-QUA; BPM-010  
**Odoo areas:** Quality, Inventory  
**Preliminary result:** **CFG / PARTIAL FIT; optional CUS for sampling and extended disposition**

### Standard capability expected to fit
- Quality control points and checks.
- Inspection records linked to stock operations.
- Quality alerts and recorded outcomes, subject to configuration.
- Stock segregation through quality/quarantine locations.

### Configuration required
- Product/category-specific incoming and outgoing inspection applicability.
- Checklist parameters and pass/fail criteria.
- Quality control points for receipt and delivery operations.
- User groups and quality roles.
- Disposition locations and permissions.

### Potential gaps
- Sampling quantity rules (5 / 10 / 20 sample units by shipment size) may need a manual SOP or custom calculation.
- Critical defect behavior must place affected quantity/lot on hold; verify whether the standard quality flow and stock locations enforce the required hard block.
- The distinction between inspector recommendation and commercial/financial write-off approval must be enforced through roles.

### Recommendation
Start with standard quality control points and checks. Use controlled manual sampling if acceptable. Develop sampling automation only if the business confirms that automated calculation and enforcement are required.

### Validation scenarios
- Incoming mandatory check generated for applicable products.
- Critical defect quarantines affected stock.
- Pending/failed stock cannot be picked for normal sales.
- Outgoing failed inspection blocks dispatch.
- Quality source records feed vendor scorecard calculations.

**Decision owner:** Operations Manager / Quality Owner  
**Priority:** Must for inspection and quarantine; sampling automation Should

---

## 6.10 Logistics and Delivery Management

**FSD references:** FSD-LOG-001 to FSD-LOG-006  
**Odoo areas:** Sales, Inventory, Documents/Chatter  
**Preliminary result:** **CFG / PARTIAL FIT**

### Standard capability expected to fit
- Delivery operation linked to sales order.
- Scheduled dates and validation timestamps.
- Attachments and chatter for POD evidence.
- Delivery status from stock operation lifecycle.

### Potential gaps
- Actual delivery date may differ from stock validation date; the FSD allows a custom field if required.
- Structured delivery discrepancy reason, quantity, evidence, and resolution may require additional fields/workflow.
- Delivery KPIs require clear date rules and partial-delivery treatment.

### KPI definitions in FSD
- On-Time Delivery Rate = on-time deliveries ÷ total completed deliveries × 100.
- Delivery Fulfillment Rate = delivered quantity ÷ ordered quantity × 100.
- Delivery Discrepancy Rate = deliveries with discrepancy ÷ total completed deliveries × 100.

### Recommendation
Use standard delivery records and attachments first. Add only the minimum structured fields and report calculations required by approved definitions. Full TMS, route optimization, fleet tracking, and live carrier integration remain out of scope.

### Validation scenarios
- Attach and retrieve POD.
- Record actual delivery date independently where required.
- Record and resolve discrepancy.
- Test partial delivery KPI calculation and promised date logic.

**Decision owner:** Operations Manager  
**Priority:** POD and delivery traceability Must; enhanced KPI Should

---

## 6.11 Customer Returns, Refunds, and Supplier Returns

**FSD references:** FSD-RET; E2E-007  
**Odoo areas:** Inventory, Sales, Purchase, Accounting  
**Preliminary result:** **CFG for physical/financial return flow; CUS candidate for refund approval**

### Standard capability expected to fit
- Return transfers referencing original delivery/receipt where supported by the transaction flow.
- Return locations and quarantine handling.
- Customer credit notes and vendor credits.
- Payment registration and reconciliation.

### Configuration required
- Return reason codes.
- Returns and quarantine locations.
- Quality inspection and disposition roles.
- Credit note and vendor credit process.
- Return access rights.

### Gap: refund approval
The FSD defines refund approval tiers:

| Refund Value | Required Approval |
|---|---|
| Up to IDR 5,000,000 | Customer Service Supervisor and Finance review |
| Above IDR 5,000,000–25,000,000 | Finance Manager |
| Above IDR 25,000,000–100,000,000 | Finance Manager and Operations Manager |
| Above IDR 100,000,000 | Managing Director and Finance Manager |

A return authorization is not the same as a financial refund approval. The approval must be linked to the credit note/refund execution and block execution until authorized.

### Recommendation
Use standard returns and credit notes. Implement a dedicated approval control only for the financial refund action. Ensure the physical return can be received and inspected without prematurely issuing a refund.

### Validation scenarios
- Customer return linked to original delivery/invoice.
- Returned goods received into quarantine.
- Disposition determines whether stock can be restocked.
- Refund approval thresholds and boundary tests.
- Supplier return links to PO/receipt and vendor credit.

**Open decisions:** Refund gross/net basis, credit note vs cash refund, approval timing, Finance review meaning.  
**Decision owner:** Finance Manager / Customer Service Owner  
**Priority:** Must

---

## 6.12 Accounting and Financial Management

**FSD references:** FSD-ACC-001 to FSD-ACC-010  
**Odoo area:** Accounting / Invoicing  
**Preliminary result:** **FIT / CFG; PARTIAL FIT for matching controls and localization confirmation**

### Standard capability expected to fit
- Customer invoices and credit notes.
- Vendor bills and vendor credits.
- AR/AP balances and aging.
- Payment registration and reconciliation.
- General ledger, trial balance, P&L, balance sheet, cash/bank reporting.
- Inventory valuation accounting when correctly configured.

### Configuration required
- Company accounting settings, chart of accounts, journals, payment terms, fiscal settings, taxes, accounts, stock interim/valuation accounts.
- Automated valuation and COGS behavior.
- Reconciliation and financial report setup.
- Access and posting rights.

### Potential gaps / dependencies
- Three-way matching tolerances and approval locks may require extension.
- Indonesian localization and statutory tax mapping must be inspected in the target database and validated by Finance/tax professionals.
- The FSD's illustrative 11% tax assumption must not be treated as current legal tax advice or copied to a production company without review.

### Recommendation
Keep accounting entries in standard Odoo accounting objects. Any custom matching layer must call/guard the standard posting flow rather than create a parallel payable ledger.

### Validation scenarios
- Post sales invoice and verify AR/revenue/tax.
- Post vendor bill and verify AP/expense or stock interim accounts.
- Reconcile customer and vendor payments.
- Reconcile stock valuation to GL.
- Validate COGS recognition.
- Confirm localization/tax setup with Finance.

**Decision owner:** Finance Manager  
**Priority:** Must

---

## 6.13 Landed Cost Management

**FSD references:** FSD-LC; E2E-008  
**Odoo areas:** Inventory Landed Costs, Accounting  
**Preliminary result:** **CFG / PARTIAL FIT**

### Standard capability expected to fit
- Landed cost records linked to eligible receipts.
- Additional cost lines.
- Allocation by supported methods, subject to Odoo 19 environment verification.
- Valuation and accounting impact on validation.

### Allocation policy in FSD

| Cost Component | Allocation Method |
|---|---|
| International Freight | By weight |
| Insurance | By current cost |
| Customs-related charges | By current cost |
| Port Handling | By quantity |
| Domestic Transportation | By weight |

### Configuration required
- Landed cost products/cost types.
- Eligible receipt selection.
- Cost allocation methods.
- Accounting accounts and journal behavior.
- Finance permissions.

### Potential gaps
- Treatment of already-sold quantities, closed accounting periods, duplicate charges, and reconciliation tolerances requires explicit confirmation.
- If an allocation method or business rule cannot be met by standard landed-cost behavior, assess a targeted extension rather than a separate cost ledger.

### Validation scenarios
- Allocate each cost type using the specified method.
- Confirm allocated total equals source charge, subject to documented rounding.
- Reconcile valuation and accounting entries.
- Test receipt with partially sold stock and closed-period edge cases.

**Decision owner:** Finance Manager  
**Priority:** Must

---

## 6.14 Vendor Performance Management

**FSD references:** FSD-VPM; E2E-010  
**Odoo areas:** Purchase, Inventory, Quality, Reporting  
**Preliminary result:** **CUS — Custom KPI calculation and scorecard likely required**

### Required KPIs
- On-Time Delivery: on-time eligible receipts ÷ total eligible receipts × 100.
- Order Fulfillment: accepted quantity received ÷ quantity due in period × 100.
- Quality Acceptance: accepted quantity ÷ inspected quantity × 100.
- Lead Time Reliability: receipts within lead-time tolerance ÷ eligible receipts × 100.
- Purchase Price Variance: (actual unit price − reference unit price) ÷ reference unit price × 100.

Weighted score:
`Vendor Score = (OTD × 30%) + (Fulfillment × 25%) + (Quality Acceptance × 30%) + (Lead Time Reliability × 15%)`

Classification:
- 95%–100%: Excellent.
- 90%–94.99%: Good.
- 80%–89.99%: Needs Improvement.
- Below 80%: Poor.
- Fewer than five eligible receipts: `Insufficient Data`, no definitive classification.

### Gap
These are cross-document calculations with period cut-off, receipt eligibility, inspection data, due quantity, reference price, formula version, and scheduled refresh requirements. Standard purchase and quality transactions provide source data but do not by themselves constitute the complete ADN scorecard.

### Proposed treatment
Build a custom scorecard/reporting layer only after the KPI rules are signed off. Preserve source links to PO, receipt, and quality records. Store calculation period, refresh timestamp, formula version, and status. Display Purchase Price Variance separately from the weighted score.

### Validation scenarios
- Fewer than five eligible receipts.
- Exact score classification boundaries.
- Partial receipt and rejected quantity.
- Late receipt and promised-date amendment.
- Missing quality inspection data.
- Reference price changes during evaluation period.
- Monthly and rolling-three-month results reconcile to transaction-level detail.

**Open decisions:** Period cut-off, promised date changes, eligible receipt definition, reference price source and effective date.  
**Decision owner:** Procurement Manager  
**Priority:** Must

---

## 6.15 Management Reporting and Business Intelligence

**FSD references:** FSD-RPT; RPT-001 to RPT-017  
**Odoo areas:** Standard reports, list/pivot/graph views, Accounting, Inventory, Sales, Purchase  
**Preliminary result:** **FIT / CFG for standard operational reports; PARTIAL FIT/CUS for consolidated KPI dashboards**

### Expected standard fit
- Inventory on-hand and movement reports.
- Sales and purchase analysis.
- AR/AP aging and financial statements.
- Standard list, pivot, graph, and export capabilities where available.

### Potential gaps
- Consolidated dashboards combining several apps and custom formulas.
- Inventory aging based on time since receipt.
- Vendor scorecard.
- Credit exposure and approval audit reports.
- Delivery discrepancy and productivity measures when time data is not captured.

### Recommendation
Use standard Odoo reports first. Build custom dashboards only for measures that cannot be reliably produced through standard views. Every KPI must specify:
- Formula.
- Source model/records.
- Date basis.
- Included and excluded states.
- Warehouse/company scope.
- Refresh frequency.
- Rounding rule.
- Drill-down path.
- Data completeness indicator.

Do not label picking/packing productivity as units per hour unless time data is captured.

### Validation scenarios
- Draft/cancelled invoices excluded from net sales.
- Posted credit notes reduce net sales.
- Tax excluded from net sales.
- Quarantined/damaged stock separated from available stock.
- Inventory valuation reconciles to accounting.
- Incomplete data displays `Insufficient Data`, `Not Available`, or `Pending Reconciliation`.
- Dashboard access respects role permissions.

**Decision owner:** ERP Reporting Owner / Finance Manager  
**Priority:** Standard reports Must; consolidated dashboards Should

---

## 6.16 Security, Approval, and Segregation of Duties

**FSD references:** FSD-SEC; Section 11 approval matrices  
**Odoo areas:** Users, Groups, ACLs, Record Rules, chatter, approved custom workflow addons  
**Preliminary result:** **CFG for basic access; CUS for business-specific approval engine**

### Standard capability expected to fit
- User groups and application permissions.
- Access control lists and record rules.
- Restricted access to accounting, purchase, sales, and warehouse operations.
- Chatter and document history for supported records.

### Configuration required
- Role matrix for Managing Director, Operations Manager, Procurement Manager, Sales Manager, Finance Manager, Warehouse Manager, Warehouse Supervisor, Inventory Controller, Sales Representative, and other FSD roles.
- Warehouse and company access restrictions.
- Create/read/write/delete permissions.
- Separation of requester and approver roles.

### Potential gap
The FSD requires several transaction-specific approval matrices, re-evaluation after amendment, self-approval prevention, and server-side execution locks. Basic Odoo groups alone should not be assumed to provide all of this.

### Recommendation
Use a reusable approval framework with:
- Approval request linked to source record.
- Requester and approver identities.
- Policy/tier and rule version.
- Pending/approved/rejected state.
- Decision timestamp and comments.
- Rejection/resubmission history.
- Before/after values for amendments.
- Server-side action lock.
- Re-approval when policy-relevant values change.
- No self-approval where prohibited.

### Validation scenarios
- Unauthorized user attempts approval.
- Requester attempts own approval.
- Approver role is changed or removed while request is pending.
- Source transaction is amended after approval.
- API/import action attempts to bypass approval.
- Approval history remains available after cancellation.

**Decision owner:** ERP Project Manager / Department Managers  
**Priority:** Must

---

## 6.17 Data Migration and Opening Data

**FSD references:** FSD-MIG; FSD-MD  
**Odoo areas:** Standard import functions and controlled staging utilities  
**Preliminary result:** **CFG / MAN**

### Expected standard fit
- Import of master records using supported import templates.
- Import of opening stock and accounting data using approved migration procedures.
- Validation through reconciliation reports and exception logs.

### Required sequence
1. UoM and product categories.
2. Warehouses and locations.
3. Vendors and customers.
4. Products.
5. Vendor/customer pricelists.
6. Lots/serials and opening inventory.
7. Opening financial balances and other approved opening data.
8. User-role staging and secure provisioning.

### Potential gaps / decisions
- Exact historical transaction migration versus opening balance approach is not confirmed.
- Migration cut-off, data owners, duplicate resolution, and reconciliation tolerances need approval.
- Passwords must never be migrated as plaintext.
- The FSD specifies a 99.5% target on a validated sample; the sampling method and error severity classification must be defined.

### Recommendation
Use controlled import templates, pre-validation, rehearsal, rejected-row reports, and signed reconciliation. Keep opening inventory and financial balances under Finance and Operations ownership.

### Validation scenarios
- Duplicate and missing references.
- Lot/serial and expiration validity.
- Opening stock quantity/value reconciliation.
- AR/AP opening balance reconciliation.
- Sample accuracy at or above approved threshold.
- Secure user provisioning.

**Decision owner:** ERP Manager / Data Owners / Finance Manager  
**Priority:** Must

---

## 6.18 Non-Functional and Operational Requirements

**FSD reference:** Section 9  
**Preliminary result:** **TBD pending infrastructure and operational design**

| Requirement | Preliminary Fit | Required Action |
|---|---|---|
| Approximately 3-second form response target | TBD | Define test profile, hardware, data volume, concurrency, and measurement |
| On-premise Ubuntu/PostgreSQL | Infrastructure design | Validate supported versions and deployment architecture |
| Backup and restore | Infrastructure / operations | Define schedule, retention, monitoring, RPO/RTO, and restore rehearsal |
| Security and auditability | CFG/CUS | Apply least privilege, audit evidence, and approval controls |
| Scalability | Architecture validation | Test projected users, warehouses, transactions, and data growth |
| Usability and training | MAN | Role-based SOPs and training acceptance |

No availability SLA, RPO, or RTO is assumed by this analysis.

---

# 7. Cross-Functional Workflow Fit Assessment

| Workflow | FSD / BPM Reference | Standard Odoo Components | Likely Gap | Fit-Gap Outcome |
|---|---|---|---|---|
| Procure to Pay | E2E-001 / BPM-004 | Purchase, Inventory, Quality, Accounting | PO approval and tolerance-based matching | CFG + CUS candidate |
| Order to Cash | E2E-002 / BPM-003 | CRM, Sales, Inventory, Accounting | Discount approval and credit exposure hold | FIT/CFG + CUS |
| Multi-Warehouse Replenishment | E2E-003 / BPM-005/006 | Inventory routes, reordering, transfers | Transfer approval policy not fully defined | CFG / TBD |
| Lot and Expiration | E2E-004 / BPM-007/008/009 | Lots, expiration, removal strategy, stock moves | Customer-specific shelf-life enforcement | CFG + P-FIT |
| Credit Limit Violation | E2E-005 / BPM-003 | Accounting AR, Sales orders | Exposure calculation and exception lock | CUS candidate |
| Supplier Delivery Discrepancy | E2E-006 / BPM-004/008 | Purchase receipt, quality, vendor bill | Structured discrepancy and KPI source logic | CFG + P-FIT |
| Customer Return and Refund | E2E-007 / BPM-012 | Return transfer, quality, credit note, payment | Refund approval workflow | CFG + CUS |
| Imported Goods and Landed Costs | E2E-008 / BPM-015 | Purchase, receipt, landed costs, accounting | Allocation edge cases and policy confirmation | CFG + P-FIT |
| Inventory Adjustment and Cycle Count | E2E-009 / BPM-016 | Inventory count/adjustment | Value-tier approval and validation lock | CUS candidate |
| Vendor Performance | E2E-010 / BPM-017 | Purchase, receipt, quality | Cross-domain KPI calculation and scorecard | CUS |

---

# 8. Customization and Extension Backlog

The backlog below is a candidate list. Final development scope is subject to fit-gap validation, approval, and TDD.

| Candidate ID | Capability | Preliminary Decision | Priority | Functional Scope | Key Controls / Acceptance |
|---|---|---|---|---|---|
| CUS-001 | Reusable Approval Framework | CUS candidate | Must | Approval requests, tiers, approvers, state, comments, history, re-submission | Server-side lock, self-approval prevention, amendment re-evaluation |
| CUS-002 | PO Approval Policy | CUS candidate using CUS-001 | Must | Untaxed PO total after line discounts; tier routing | Boundary tests, requester/approver separation |
| CUS-003 | Sales Discount Approval | CUS candidate using CUS-001 | Must | Per-line discount tier and approval status | Multi-line and amendment tests |
| CUS-004 | Credit Exposure and Hold | CUS candidate | Must | Exposure calculation, warning, hold, exception release | Reconciliation to AR/orders; no double count |
| CUS-005 | Inventory Adjustment Approval | CUS candidate using CUS-001 | Must | Absolute valuation difference and approver tier | Value boundary, aggregation, valuation test |
| CUS-006 | Refund Approval | CUS candidate using CUS-001 | Must | Refund tier and execution lock | Credit note/refund accounting test |
| CUS-007 | Vendor Scorecard | CUS | Must | KPI calculation, weighted score, classification, insufficient-data state | Formula, period, sample, source drill-down tests |
| CUS-008 | Consolidated Management Dashboards | CUS candidate | Should | Cross-domain KPI views and drill-down | Formula and reconciliation sign-off |
| CUS-009 | Shelf-Life Validation | CUS candidate | Should | Customer/order-specific minimum shelf-life check | Expiry boundary and override tests |
| CUS-010 | Quality Sampling Extension | CUS candidate | Should | Sample quantity calculation and checklist fields | Sampling and critical defect tests |
| CUS-011 | Delivery Discrepancy Fields | CUS candidate | Should | Reason, quantity, evidence, resolution | Delivery KPI reconciliation |
| CUS-012 | Stock Aging Enhancement | CUS candidate | Should | Aging buckets based on approved receipt/valuation basis | Reconcile to stock source |
| INT-001 | External System Interface | Not currently approved | TBD | Only explicitly authorized data exchange | Separate interface scope, security, retry, monitoring |

## 8.1 Reusable Approval Framework — Recommended Functional Pattern

To reduce duplicated custom logic, evaluate one reusable approval service for CUS-001 through CUS-006.

Minimum functional elements:
- Source model and source record identifier.
- Approval policy identifier and version.
- Requester, submission timestamp, and reason.
- Amount/value basis and calculated tier.
- Required approver role(s) and assigned approver(s).
- Approval state and decision history.
- Comments and evidence attachments.
- Rejection and resubmission handling.
- Server-side validation before the controlled action.
- Re-evaluation when relevant source values change.
- Audit record retained after cancellation.

The TDD must decide whether the framework is a shared addon or separate modules using a common service. This FGA does not prescribe the technical architecture.

## 8.2 Customization Non-Goals

Customizations must not:
- Replace standard Odoo sales, purchase, stock, or accounting documents.
- Create a second stock ledger or general ledger.
- Allow approval state to be bypassed through import, RPC/API, automated actions, or direct workflow transitions.
- Hard-code policy thresholds where controlled configuration is feasible.
- Present unverified KPI values as actual.
- Implement out-of-scope TMS, fleet tracking, bank connectivity, or marketplace integration without change approval.

---

# 9. Configuration Workstream

| Config ID | Configuration Area | Key Activities | Owner | Dependency |
|---|---|---|---|---|
| CFG-001 | Company / Accounting Foundation | Company, currency, fiscal settings, chart of accounts, journals | Finance | Tax/localization decision |
| CFG-002 | Master Data | Categories, UoM, product/customer/vendor fields, identifiers | Data Owners | Migration templates |
| CFG-003 | Warehouses / Locations | WH-JKT, WH-BDG, WH-SBY and internal location hierarchy | Operations | Warehouse layout |
| CFG-004 | Inventory Tracking | Lot/serial, expiration, removal strategy, reservation | Inventory Controller | Product master |
| CFG-005 | Costing / Valuation | FIFO/AVCO categories, automated valuation, accounts | Finance | Accounting prototype |
| CFG-006 | Replenishment | Min/max, routes, vendor lead times, internal supply | Procurement / Operations | Stock planning policy |
| CFG-007 | Quality | Control points, checklist, inspection triggers, dispositions | Quality Owner | Product applicability |
| CFG-008 | Sales | Pricelists, payment terms, warehouses, invoicing policy | Sales | Customer master |
| CFG-009 | Purchase | RFQ, vendor data, receipt controls, bill controls | Procurement | Vendor master |
| CFG-010 | Security | Groups, ACLs, record rules, warehouse access | ERP Manager | Approved role matrix |
| CFG-011 | Reporting | Standard views, filters, export, report access | Reporting Owner | KPI definitions |
| CFG-012 | Documents / Evidence | Attachment policy, POD, inspection evidence | ERP Manager | Retention policy |

---

# 10. Business Decisions and Open Questions

These decisions must be closed before the related feature is approved for build. The source FSD identifies DEC-001 through DEC-012; this FGA preserves those topics and adds implementation questions needed for validation.

| Decision ID | Topic | Required Decision / Clarification | Owner | Impact if Unresolved |
|---|---|---|---|---|
| DEC-001 | Purchase Approval | Confirm approver routing, delegation, substitution, amendment behavior, and split-order monitoring | Procurement Manager | PO approval design and tests |
| DEC-002 | Sales Discount | Confirm discount reference price, rounding, cumulative discounts, line/order scope, reapproval | Sales Manager | Discount approval logic |
| DEC-003 | Inventory Adjustment | CLOSED (2026-11-22): valuation cost; per-line currency rounding; sum of absolute line values; company + warehouse + accounting-date grouping; submission snapshot/release revalidation; parallel all-required approval | Operations + Finance | Adjustment approval logic |
| DEC-004 | Costing | Validate FIFO/AVCO by category, automated valuation, accounts, and change restrictions | Finance Manager | Inventory valuation and migration |
| DEC-005 | Indonesian Tax | Confirm localization, tax mapping, rates, reporting, and professional review | Finance Manager | Accounting configuration |
| DEC-006 | Credit Management | Confirm exposure sources, order/invoice overlap, trigger, exception expiry, concurrent orders | Finance Manager | Credit calculation and hold |
| DEC-007 | Quality | Confirm checklist representation, sampling execution, defect severity, disposition authority | Operations / Quality | Quality configuration/customization |
| DEC-008 | Vendor Performance | Confirm date rules, due quantity logic, reference price, period cut-off, sample rule | Procurement Manager | Vendor scorecard |
| DEC-009 | Reporting | Confirm KPI date basis, model, refresh, reconciliation, audience, and filters | Reporting Owner | Dashboard design |
| DEC-010 | Data Migration | Confirm import templates, opening balances, historical transactions, cut-off | ERP Manager / Finance | Migration scope and rehearsal |
| DEC-011 | Refund Approval | Confirm gross/net basis, credit note vs cash refund, Finance review, execution point | Finance Manager | Refund workflow |
| DEC-012 | Landed Cost | Confirm eligible costs, allocation methods, already-sold quantities, period treatment | Finance Manager | Landed-cost configuration |
| DEC-013 | Shelf-Life Exception | Confirm who can override minimum remaining shelf life and with what evidence | Operations / Sales | Allocation validation |
| DEC-014 | Transfer Authority | Define when inter-warehouse transfers require approval and by what value/quantity | Operations Manager | Transfer workflow |
| DEC-015 | Delivery KPI | Define promised date, partial-delivery treatment, completion date, and discrepancy criteria | Operations Manager | Delivery dashboard |
| DEC-016 | Data Retention | Define retention and audit requirements for approval, POD, quality, and attachments | ERP Manager | Evidence design |
| DEC-017 | Performance Test | Define hardware, concurrency, dataset, and response measurement for 3-second target | Technical Lead | Infrastructure sizing |

---

# 11. Risks, Dependencies, and Mitigations

| Risk ID | Risk | Impact | Mitigation | Owner |
|---|---|---|---|---|
| RSK-001 | Standard feature assumed to fit without target-environment proof | Rework / scope gap | E1–E3 validation before design baseline | Functional Lead |
| RSK-002 | Excessive custom approval logic | Upgrade and maintenance burden | Reusable approval framework; configuration-first review | Technical Lead |
| RSK-003 | Approval bypass through API/import | Financial or operational control failure | Server-side enforcement and negative tests | Technical Lead |
| RSK-004 | Incorrect credit exposure calculation | Uncontrolled customer credit | Reconcile formula to AR and open orders; concurrency tests | Finance |
| RSK-005 | Costing / valuation misconfiguration | GL and stock valuation mismatch | Finance-led prototype and reconciliation | Finance |
| RSK-006 | Incorrect tax localization assumptions | Compliance risk | Current professional validation; no production use of dummy rates | Finance |
| RSK-007 | Poor master data quality | Failed transactions and migration rework | Data profiling, validation, ownership, rehearsal | Data Owners |
| RSK-008 | Incomplete quality/expiry rules | Expired or defective stock dispatched | Mandatory tests and stock segregation | Operations |
| RSK-009 | KPI source data incomplete or ambiguous | Misleading management reporting | Signed formulas, completeness states, drill-down | Reporting Owner |
| RSK-010 | Unclear migration cut-off and opening balances | Financial/stock imbalance | Reconciliation sign-off and controlled cut-over | Finance / ERP Manager |
| RSK-011 | Optional app/device not licensed or available | Warehouse process cannot be executed as designed | Confirm entitlements and devices early | Project Manager |
| RSK-012 | Backup/performance design not validated | Operational continuity risk | Infrastructure design, load test, restore rehearsal | Technical Lead |

## 11.1 Key Dependencies

- Confirmed Odoo 19 Enterprise edition, licensed applications, and installed modules.
- Representative target database for configuration and prototype.
- Approved role and approval matrix.
- Clean product, customer, vendor, and warehouse data.
- Finance-approved chart of accounts, valuation accounts, and localization.
- Confirmed tax assumptions and professional review.
- Warehouse location layouts and physical operating procedures.
- Defined KPI formulas and data owners.
- Approved migration cut-off and opening balance strategy.
- Infrastructure sizing and backup/restore plan.

---

# 12. Validation and Acceptance Plan

## 12.1 Validation Approach

| Stage | Activity | Evidence | Exit Criteria |
|---|---|---|---|
| E1 | Inspect target Odoo environment | App list, edition, installed modules, settings, localization | Dependencies documented |
| E2 | Configure prototype | Configuration workbook and demo records | Standard/configuration capability demonstrated |
| E3 | Execute fit-gap tests | Test results, screenshots/logs, source record links | Functional and negative tests pass |
| E4 | Process owner review | Workshop minutes and decision log | Business behavior accepted |
| E5 | Baseline design | Approved FGA and updated FSD | TDD/build scope authorized |

## 12.2 Minimum Fit-Gap Test Catalogue

| Test ID | Area | Test | Expected Result |
|---|---|---|---|
| FGA-MD-001 | Master Data | Import duplicate product reference | Duplicate rejected and logged |
| FGA-MD-002 | Master Data | Import missing category/UoM | Dependent row rejected or held |
| FGA-CRM-001 | CRM | Lead to opportunity to quotation | Linked records and activity history |
| FGA-SAL-001 | Sales | Customer-specific pricelist | Expected price proposed |
| FGA-SAL-002 | Discount | Test 5%, 5.01%, 10%, 10.01%, 15%, 15.01% | Correct tier and approval state |
| FGA-SAL-003 | Discount | Amend approved line | Reapproval required where policy says so |
| FGA-CRD-001 | Credit | Exposure at 80%, above 80%, 100%, above 100% | Correct normal/warning/hold behavior |
| FGA-CRD-002 | Credit | Convert order exposure to invoice | No double counting |
| FGA-PUR-001 | Purchase | PO at each approval boundary | Correct approver tier |
| FGA-PUR-002 | Purchase | Self-approval attempt | Denied |
| FGA-PUR-003 | Purchase | Amend PO into higher tier | Approval recalculated |
| FGA-PUR-004 | Matching | Quantity variance at 2% and above 2% | Correct match/exception |
| FGA-PUR-005 | Matching | Price variance at 1% and above 1% | Correct match/exception |
| FGA-SUP-001 | Replenishment | Min/max by warehouse | Independent replenishment proposal |
| FGA-SUP-002 | Transfer | Partial dispatch/receipt | Correct transit and remaining quantity |
| FGA-INV-001 | Inventory | Lot and serial receipt | Traceability preserved |
| FGA-INV-002 | FEFO | Eligible lots with different expiry dates | Earliest eligible lot selected |
| FGA-INV-003 | Expiry | Expired and shelf-life-ineligible lot | Excluded or blocked as approved |
| FGA-INV-004 | Costing | FIFO/AVCO category receipt and delivery | Expected valuation and GL |
| FGA-INV-005 | Adjustment | Each value approval boundary | Correct approval and validation lock |
| FGA-WH-001 | Warehouse | Partial receipt and delivery | Backorder/outstanding quantity retained |
| FGA-QUA-001 | Quality | Critical defect on incoming lot | Affected quantity quarantined |
| FGA-QUA-002 | Quality | Mandatory outgoing inspection fails | Dispatch blocked |
| FGA-LOG-001 | Logistics | Attach POD and record discrepancy | Evidence retrievable and reportable |
| FGA-RET-001 | Returns | Customer return to quarantine | Return linked and not sellable pending inspection |
| FGA-RET-002 | Refund | Each refund threshold | Correct approval and execution lock |
| FGA-ACC-001 | Accounting | Post customer invoice and payment | AR/revenue/tax and reconciliation correct |
| FGA-ACC-002 | Accounting | Post vendor bill and payment | AP and reconciliation correct |
| FGA-LC-001 | Landed Cost | Allocate each cost type | Total allocation reconciles |
| FGA-VPM-001 | Vendor KPI | Fewer than five eligible receipts | Insufficient Data |
| FGA-VPM-002 | Vendor KPI | Weighted score boundaries | Correct classification |
| FGA-RPT-001 | Reporting | Draft invoice in net sales | Excluded |
| FGA-RPT-002 | Reporting | Posted credit note | Reduces net sales |
| FGA-SEC-001 | Security | Unauthorized approval attempt | Denied and auditable |
| FGA-MIG-001 | Migration | Validated migration sample | Meets approved accuracy target |

## 12.3 Fit-Gap Exit Criteria

The FGA can be baselined when:
- Every Must requirement has a recorded fit-gap outcome.
- Every CUS item has an approved functional scope and business owner.
- Every OPEN DECISION has a named owner and target resolution date.
- Odoo edition, installed apps, and dependencies are confirmed.
- Standard/configuration prototypes have been demonstrated for critical workflows.
- Customization candidates have been reviewed for upgrade and security impact.
- Acceptance tests and source traceability are defined.
- Scope changes are recorded through formal change control.

---

# 13. Implementation Recommendation and Next Steps

## 13.1 Recommended Work Sequence

1. **Environment and entitlement validation:** inspect Odoo 19 Enterprise edition, apps, localization, and installed modules.
2. **Policy workshops:** close DEC-001 through DEC-017, prioritizing approval, credit, costing, tax, and landed cost.
3. **Standard configuration prototype:** master data, CRM, Sales, Purchase, Inventory, Quality, Accounting, and reporting.
4. **Fit-gap test execution:** execute E1–E3 evidence for core workflows and boundary controls.
5. **Customization approval:** confirm CUS backlog, priorities, scope, and ownership.
6. **TDD preparation:** design approved custom workflows, models, validations, security, scheduled jobs, and reporting.
7. **Build and unit testing:** implement approved extensions and automated tests.
8. **End-to-end integration testing:** validate P2P, O2C, inventory, quality, returns, landed cost, and vendor scorecard.
9. **Migration rehearsal and reconciliation:** validate master data, opening stock, and financial balances.
10. **UAT and operational readiness:** execute role-based scenarios, train users, and close critical defects.

## 13.2 Recommended Build Priorities

**Must-have before controlled UAT**
- Purchase approval.
- Sales discount approval.
- Credit exposure and hold.
- Inventory adjustment approval.
- Refund approval.
- Vendor scorecard.
- Core accounting/valuation configuration.
- Warehouse/lot/expiry/quality controls.
- Security and audit controls.

**Should-have subject to confirmed fit**
- Consolidated management dashboards.
- Shelf-life validation extension.
- Quality sampling automation.
- Delivery discrepancy enhancement.
- Stock aging enhancement.

**Not in current baseline**
- Full TMS, fleet tracking, route optimization.
- Live carrier, bank, marketplace, or payment gateway integration.
- Manufacturing, MRP, HR, payroll, and robotics.
- AI forecasting and external customs brokerage integration.

## 13.3 Handover to TDD

The TDD should receive:
- Approved fit-gap register and decision log.
- Approved customization backlog.
- Detailed workflow and state transitions.
- Security/role matrix and record access rules.
- Approval threshold and formula definitions.
- Data model and source-record linkage requirements.
- Scheduled job/report requirements.
- Exception and error-handling rules.
- Test cases and acceptance criteria.
- Deployment, upgrade, monitoring, and rollback considerations.

---

# 14. Requirements Traceability Matrix — Summary

| FSD Domain | Fit-Gap IDs | Outcome | Next Deliverable |
|---|---|---|---|
| Master Data | GAP-MD-001 | CFG | Configuration workbook / migration mapping |
| CRM | GAP-CRM-001 | FIT/CFG | CRM configuration and test evidence |
| Sales / O2C | GAP-SAL-001, GAP-SAL-002 | FIT/CFG + CUS candidate | Sales configuration and discount workflow TDD |
| Credit | GAP-CRD-001 | CUS candidate | Credit rule specification |
| Procurement / P2P | GAP-PUR-001, GAP-PUR-002, GAP-PUR-003 | CFG/P-FIT + CUS candidate | Purchase configuration and approval/matching TDD |
| Replenishment / Transfer | GAP-SUP-001, GAP-SUP-002 | CFG/TBD | Warehouse route design |
| Inventory / Costing | GAP-INV-001 to GAP-INV-005 | CFG/P-FIT + CUS candidate | Inventory configuration and adjustment workflow TDD |
| Warehouse Execution | GAP-WH-001 | FIT/CFG | Warehouse configuration and SOP |
| Quality | GAP-QUA-001, GAP-QUA-002 | CFG/P-FIT | Quality configuration and sampling decision |
| Logistics | GAP-LOG-001, GAP-LOG-002 | CFG/P-FIT | Delivery field/KPI specification |
| Returns | GAP-RET-001, GAP-RET-002 | CFG + CUS candidate | Returns configuration and refund workflow TDD |
| Accounting | GAP-ACC-001, GAP-ACC-002 | FIT/CFG/TBD | Finance configuration and localization review |
| Landed Cost | GAP-LC-001 | CFG/P-FIT | Landed cost configuration/test evidence |
| Vendor Performance | GAP-VPM-001 | CUS | Scorecard functional/technical design |
| Reporting | GAP-RPT-001 | FIT/CFG/CUS candidate | KPI catalogue and dashboard specification |
| Security | GAP-SEC-001 | CFG/CUS | Role matrix and approval security design |
| Migration | GAP-MIG-001 | CFG/MAN | Migration strategy and reconciliation plan |
| Non-Functional | GAP-NFR-001 | TBD | Infrastructure and operational design |

---

# 15. Glossary

| Term | Definition |
|---|---|
| Fit | Requirement expected to be satisfied by standard Odoo behavior |
| Configuration | Setup of standard Odoo features without changing core code |
| Partial Fit | Standard feature satisfies only part of the requirement |
| Gap | Difference between required business behavior and demonstrated system behavior |
| Customization | Approved extension/addon that adds or changes functional behavior |
| Integration | Controlled exchange of data with an external system |
| FSD | Functional Specification Document |
| FGA | Fit-Gap Analysis |
| TDD | Technical Design Document |
| O2C | Order to Cash |
| P2P | Procure to Pay |
| FEFO | First Expired, First Out |
| FIFO | First In, First Out |
| AVCO | Average Cost |
| POD | Proof of Delivery |
| SoD | Segregation of Duties |
| KPI | Key Performance Indicator |
| UAT | User Acceptance Testing |
| ACL | Access Control List |
| RPO | Recovery Point Objective |
| RTO | Recovery Time Objective |

---

# 16. FGA Completion and Approval

This document is a preliminary fit-gap assessment. Its classifications must be updated based on target-environment inspection, configuration prototypes, functional tests, and business-owner decisions.

| Role | Responsibility | Status |
|---|---|---|
| Project Sponsor / Managing Director | Approve business policy and material scope decisions | Pending |
| Operations Manager | Approve operational fit-gap outcomes | Pending |
| Procurement Manager | Approve procurement and vendor management outcomes | Pending |
| Sales Manager | Approve CRM, sales, pricing, and discount outcomes | Pending |
| Finance Manager | Approve credit, accounting, costing, tax assumptions, refunds, and landed costs | Pending |
| ERP Functional Lead | Confirm functional configuration and fit-gap evidence | Pending |
| ERP Technical Lead | Confirm technical feasibility and customization approach | Pending |
| ERP Project Manager | Baseline document and manage change control | Pending |

**End of Document**
