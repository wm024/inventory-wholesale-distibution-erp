# REQUIREMENTS TRACEABILITY MATRIX (RTM)
## Odoo 19 Enterprise ERP — Advanced Wholesale Distribution & Supply Chain

**Company:** PT Arunika Distribusi Nusantara  
**Project ID:** ADN-ERP-2026-001  
**Document ID:** ADN-RTM-001  
**Version:** 1.0  
**Date:** 19 November 2026  
**Status:** Approved Baseline — Derived from Approved FSD, Fit-Gap Analysis, and Technical Design  
**ERP Platform:** Odoo 19 Enterprise  
**Deployment:** On-Premise | Ubuntu Linux | PostgreSQL  
**Primary Currency:** IDR  
**Classification:** Portfolio / Fictional Business Case

> **Portfolio disclaimer:** PT Arunika Distribusi Nusantara and its business scenario, policies, sample thresholds, and data volumes are fictional. This RTM is a controlled traceability artifact for the approved project baseline; it does not evidence a live production deployment or executed test results.

---
# 1. Document Control
## 1.1 Purpose
This Requirements Traceability Matrix establishes bidirectional traceability from approved business and functional requirements through the approved Fit-Gap decisions, technical design components, test coverage, and acceptance evidence. It is the control register for scope completeness, implementation coverage, verification, and change impact analysis.

## 1.2 Approved Baseline Register
| Baseline Document | Document ID | Version | Baseline Status | RTM Usage |
|---|---|---:|---|---|
| Functional Specification Document | ADN-FSD-001 | 1.0 | **Approved** (per project instruction) | Authoritative functional requirement IDs, rules, process behavior, acceptance criteria |
| Fit-Gap Analysis | ADN-FGA-001 | 1.0 | **Approved** (per project instruction) | Standard/configuration/customization classification, customization backlog CUS-001–CUS-012, open decision register |
| Technical Design Document | ADN-TDD-001 | 1.0 | **Approved** (per project instruction) | Addon architecture, data model, approval engine, security, workflows, test design and deployment controls |
| Business Process Mapping | ADN-BPM-001 | 1.0 | Reference baseline | End-to-end process context and process ownership |
| Business Requirements Document | ADN-BRD-001 | 1.1 | Reference baseline | Business-origin traceability where FSD references BRD sections |
| Scope of Work | ADN-SOW-001 | 1.0 | Reference baseline | Contractual scope and acceptance alignment |

**Status governance:** The Approved status above reflects the user-confirmed project governance instruction for this RTM. Earlier draft/pending labels embedded in source document front matter and approval tables are superseded for baseline-status reporting. Their historical text is not silently rewritten. Any post-approval change must be processed through formal change control.

## 1.3 Traceability Chain
`BRD / SOW → BPM Process → FSD Requirement → FGA Fit-Gap / CUS Decision → TDD Component / Data / Security / Workflow → Test Case → Execution Evidence → Acceptance / Sign-off`

## 1.4 Traceability Rules
- Original FSD requirement identifiers and wording are retained exactly as captured in the FSD requirement tables.
- Requirements not assigned a formal FSD ID are recorded as `RTM-DER-*` derived traceability items. These IDs are RTM identifiers only and do not amend the approved FSD.
- FGA customization IDs (`CUS-001` to `CUS-012`) and decision IDs (`DEC-001` to `DEC-017`) are preserved as source identifiers.
- A technical component mapping is not proof of implementation; a test reference is not proof of successful execution. Evidence fields remain Pending until actual execution artifacts are attached.
- Standard Odoo functionality remains the system of record. Custom addons extend standard transaction models and do not create parallel sales, purchase, stock, or accounting ledgers.
- A requirement is considered verified only when its acceptance criteria pass, negative/security tests pass where applicable, and evidence is reviewed by the designated owner.

# 2. Traceability Status Model and Coverage Summary
## 2.1 Status Definitions
| Status | Definition |
|---|---|
| Approved Baseline | Requirement/design is included in the approved baseline |
| Designed | Mapping exists in approved TDD; implementation is not thereby confirmed |
| Ready for Build | Dependencies and design decisions are closed; development may start |
| In Development | Coding/configuration is in progress |
| Implemented | Deployed to the target test environment and code/configuration reviewed |
| Tested – Pass / Fail | Test executed with recorded result and evidence |
| Accepted | Business/technical owner formally accepts the requirement and evidence |
| Deferred / Out of Scope | Explicitly deferred or excluded through approved governance |
| Blocked | A dependency, unresolved policy, environment issue, or defect prevents progress |

## 2.2 Baseline Coverage Inventory
- Explicitly numbered FSD functional requirements extracted: **72**.
- FGA customization backlog: **12** items (CUS-001–CUS-012).
- FGA decision register: **17** items (DEC-001–DEC-017).
- TDD technical domains traced: architecture/addon structure, approval engine, transaction adapters, data model, security/SoD, server-side workflow, automation, audit/reporting, tests, deployment and operations.
- Supplemental RTM-derived requirements cover FSD domains whose detailed controls are described in narrative tables/workflows rather than individually numbered requirement rows.

**Execution status at baseline issue:** All requirements below are Approved Baseline. Implementation, test execution, and business acceptance are **Not Yet Evidenced / Pending Execution** unless subsequently updated with controlled evidence.

# 3. Master Functional Requirements Traceability
The following register contains every explicitly numbered functional requirement found in the approved FSD v1.0 requirement tables.

| FSD Requirement ID | Approved Functional Requirement | FSD Implementation Type | Fit-Gap Treatment | Technical Design Trace | Verification / Test Reference | Lifecycle Status |
|---|---|---|---|---|---|---|
| FSD-MD-001 | Maintain unique product records | CFG | Standard Odoo + configuration | adn_master_data_controls (only approved extension) | TC-MD-001–002; master-data import and uniqueness tests | Approved Baseline; execution pending |
| FSD-MD-002 | Maintain product category hierarchy and costing policy | CFG | Standard Odoo + configuration | adn_master_data_controls (only approved extension) | TC-MD-001–002; master-data import and uniqueness tests | Approved Baseline; execution pending |
| FSD-MD-003 | Maintain customer and vendor records | CFG/CUS | Custom / configuration-dependent | Standard model controls; custom validation only where approved | TC-MD-001–002; master-data import and uniqueness tests | Approved Baseline; execution pending |
| FSD-MD-004 | Maintain multiple delivery and invoice addresses | STD | Standard Odoo | adn_master_data_controls (only approved extension) | TC-MD-001–002; master-data import and uniqueness tests | Approved Baseline; execution pending |
| FSD-MD-005 | Maintain vendor lead time and product/vendor prices | CFG | Standard Odoo + configuration | adn_master_data_controls (only approved extension) | TC-MD-001–002; master-data import and uniqueness tests | Approved Baseline; execution pending |
| FSD-MD-006 | Maintain three warehouses and internal location hierarchy | CFG | Standard Odoo + configuration | adn_master_data_controls (only approved extension) | TC-MD-001–002; master-data import and uniqueness tests | Approved Baseline; execution pending |
| FSD-MD-007 | Control master creation and amendment | CFG/CUS | Custom / configuration-dependent | Standard model controls; custom validation only where approved | TC-MD-001–002; master-data import and uniqueness tests | Approved Baseline; execution pending |
| FSD-MD-008 | Validate unique external identifiers and import references | CFG/CUS | Custom / configuration-dependent | Standard model controls; custom validation only where approved | TC-MD-001–002; master-data import and uniqueness tests | Approved Baseline; execution pending |
| FSD-MD-009 | Maintain product lot/serial and expiration settings | CFG | Standard Odoo + configuration | adn_master_data_controls (only approved extension) | TC-MD-001–002; master-data import and uniqueness tests | Approved Baseline; execution pending |
| FSD-MD-010 | Stage 20 user-role records | CFG/MAN | Standard Odoo + configuration | adn_master_data_controls (only approved extension) | TC-MD-001–002; master-data import and uniqueness tests | Approved Baseline; execution pending |
| FSD-CRM-001 | Register leads and inquiries | STD | Standard Odoo | adn_customer_segmentation (CUS-008 only if approved; otherwise scheduled reporting) | TC-CRM-001; CRM conversion and segment tests | Approved Baseline; execution pending |
| FSD-CRM-002 | Assign salesperson and sales team | CFG | Standard Odoo + configuration | adn_customer_segmentation (CUS-008 only if approved; otherwise scheduled reporting) | TC-CRM-001; CRM conversion and segment tests | Approved Baseline; execution pending |
| FSD-CRM-003 | Qualify lead and create opportunity | STD | Standard Odoo | adn_customer_segmentation (CUS-008 only if approved; otherwise scheduled reporting) | TC-CRM-001; CRM conversion and segment tests | Approved Baseline; execution pending |
| FSD-CRM-004 | Record calls, meetings, tasks, and follow-ups | STD | Standard Odoo | adn_customer_segmentation (CUS-008 only if approved; otherwise scheduled reporting) | TC-CRM-001; CRM conversion and segment tests | Approved Baseline; execution pending |
| FSD-CRM-005 | Track won/lost status and reasons | CFG | Standard Odoo + configuration | adn_customer_segmentation (CUS-008 only if approved; otherwise scheduled reporting) | TC-CRM-001; CRM conversion and segment tests | Approved Baseline; execution pending |
| FSD-CRM-006 | Create quotation from opportunity | STD | Standard Odoo | adn_customer_segmentation (CUS-008 only if approved; otherwise scheduled reporting) | TC-CRM-001; CRM conversion and segment tests | Approved Baseline; execution pending |
| FSD-CRM-007 | Classify customer segment by annual net sales | CUS/TBD | Custom / configuration-dependent | Standard reporting / scheduled calculation; confirm design boundary | TC-CRM-001; CRM conversion and segment tests | Approved Baseline; execution pending |
| FSD-CRM-008 | Allow strategic manual segment override with reason and approver | CUS | Custom / configuration-dependent | Controlled customer segment override; approval/audit pattern | TC-CRM-001; CRM conversion and segment tests | Approved Baseline; execution pending |
| FSD-SAL-001 | Create quotations and sales orders | STD | Standard Odoo | adn_approval_core + adn_sale_discount_approval; adn_credit_control | TC-SAL-001–005; TC-CRD-001–004 | Approved Baseline; execution pending |
| FSD-SAL-002 | Apply customer/category-specific pricing | CFG | Standard Odoo + configuration | adn_approval_core + adn_sale_discount_approval; adn_credit_control | TC-SAL-001–005; TC-CRD-001–004 | Approved Baseline; execution pending |
| FSD-SAL-003 | Evaluate discount approval per order line | CUS | Custom / configuration-dependent | adn_approval_core → adn_sale_discount_approval | TC-SAL-001–005; TC-CRD-001–004 | Approved Baseline; execution pending |
| FSD-SAL-004 | Require reason for exceptional pricing | CUS | Custom / configuration-dependent | adn_approval_core → adn_sale_discount_approval | TC-SAL-001–005; TC-CRD-001–004 | Approved Baseline; execution pending |
| FSD-SAL-005 | Run credit validation before order confirmation | CUS | Custom / configuration-dependent | adn_credit_control + Sales server-side gate | TC-SAL-001–005; TC-CRD-001–004 | Approved Baseline; execution pending |
| FSD-SAL-006 | Reserve stock based on configured routes and availability | CFG | Standard Odoo + configuration | adn_approval_core + adn_sale_discount_approval; adn_credit_control | TC-SAL-001–005; TC-CRD-001–004 | Approved Baseline; execution pending |
| FSD-SAL-007 | Support partial deliveries | STD | Standard Odoo | adn_approval_core + adn_sale_discount_approval; adn_credit_control | TC-SAL-001–005; TC-CRD-001–004 | Approved Baseline; execution pending |
| FSD-SAL-008 | Support lot/serial and FEFO allocation | CFG | Standard Odoo + configuration | adn_approval_core + adn_sale_discount_approval; adn_credit_control | TC-SAL-001–005; TC-CRD-001–004 | Approved Baseline; execution pending |
| FSD-SAL-009 | Create customer invoice | STD/CFG | Standard Odoo + configuration | adn_approval_core + adn_sale_discount_approval; adn_credit_control | TC-SAL-001–005; TC-CRD-001–004 | Approved Baseline; execution pending |
| FSD-SAL-010 | Register and reconcile customer payments | STD | Standard Odoo | adn_approval_core + adn_sale_discount_approval; adn_credit_control | TC-SAL-001–005; TC-CRD-001–004 | Approved Baseline; execution pending |
| FSD-SAL-011 | Trace order, delivery, invoice, credit note, and payment | STD | Standard Odoo | adn_approval_core + adn_sale_discount_approval; adn_credit_control | TC-SAL-001–005; TC-CRD-001–004 | Approved Baseline; execution pending |
| FSD-PUR-001 | Generate purchasing demand from replenishment | CFG | Standard Odoo + configuration | adn_approval_core + adn_purchase_approval; three-way-match extension only if approved | TC-PUR-001–008 | Approved Baseline; execution pending |
| FSD-PUR-002 | Prepare internal purchase request | CFG/TBD | Standard Odoo + configuration | adn_approval_core + adn_purchase_approval; three-way-match extension only if approved | TC-PUR-001–008 | Approved Baseline; execution pending |
| FSD-PUR-003 | Create and send RFQs | STD | Standard Odoo | adn_approval_core + adn_purchase_approval; three-way-match extension only if approved | TC-PUR-001–008 | Approved Baseline; execution pending |
| FSD-PUR-004 | Compare vendor offers | CFG | Standard Odoo + configuration | adn_approval_core + adn_purchase_approval; three-way-match extension only if approved | TC-PUR-001–008 | Approved Baseline; execution pending |
| FSD-PUR-005 | Maintain vendor prices and lead times | CFG | Standard Odoo + configuration | adn_approval_core + adn_purchase_approval; three-way-match extension only if approved | TC-PUR-001–008 | Approved Baseline; execution pending |
| FSD-PUR-006 | Calculate PO approval tier | CUS | Custom / configuration-dependent | adn_approval_core → adn_purchase_approval | TC-PUR-001–008 | Approved Baseline; execution pending |
| FSD-PUR-007 | Prevent PO confirmation before approval | CUS | Custom / configuration-dependent | adn_approval_core → adn_purchase_approval | TC-PUR-001–008 | Approved Baseline; execution pending |
| FSD-PUR-008 | Re-evaluate approval after amendments | CUS | Custom / configuration-dependent | adn_approval_core → adn_purchase_approval | TC-PUR-001–008 | Approved Baseline; execution pending |
| FSD-PUR-009 | Receive full or partial quantities | STD | Standard Odoo | adn_approval_core + adn_purchase_approval; three-way-match extension only if approved | TC-PUR-001–008 | Approved Baseline; execution pending |
| FSD-PUR-010 | Perform incoming quality checks | CFG | Standard Odoo + configuration | adn_approval_core + adn_purchase_approval; three-way-match extension only if approved | TC-PUR-001–008 | Approved Baseline; execution pending |
| FSD-PUR-011 | Match PO, receipt, and vendor bill | CFG/CUS | Configuration + possible approved extension | adn_approval_core + adn_purchase_approval; three-way-match extension only if approved | TC-PUR-001–008 | Approved Baseline; execution pending |
| FSD-PUR-012 | Register vendor payment and reconcile | STD | Standard Odoo | adn_approval_core + adn_purchase_approval; three-way-match extension only if approved | TC-PUR-001–008 | Approved Baseline; execution pending |
| FSD-INV-001 | Real-time inventory balances | STD | Standard Odoo | adn_inventory_adjustment_approval; optional adn_stock_aging / shelf-life extensions | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-002 | Multiple warehouses | CFG | Standard Odoo + configuration | adn_inventory_adjustment_approval; optional adn_stock_aging / shelf-life extensions | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-003 | Hierarchical locations | CFG | Standard Odoo + configuration | adn_inventory_adjustment_approval; optional adn_stock_aging / shelf-life extensions | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-004 | Lot tracking | CFG | Standard Odoo + configuration | adn_inventory_adjustment_approval; optional adn_stock_aging / shelf-life extensions | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-005 | Serial tracking | CFG | Standard Odoo + configuration | adn_inventory_adjustment_approval; optional adn_stock_aging / shelf-life extensions | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-006 | Expiration tracking | CFG | Standard Odoo + configuration | adn_inventory_adjustment_approval; optional adn_stock_aging / shelf-life extensions | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-007 | FEFO allocation | CFG | Standard Odoo + configuration | adn_inventory_adjustment_approval; optional adn_stock_aging / shelf-life extensions | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-008 | FIFO/AVCO category costing | CFG | Standard Odoo + configuration | adn_inventory_adjustment_approval; optional adn_stock_aging / shelf-life extensions | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-009 | Inventory adjustment | STD/CUS | Custom / configuration-dependent | adn_approval_core → adn_inventory_adjustment_approval | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-010 | Cycle counting | CFG | Standard Odoo + configuration | adn_inventory_adjustment_approval; optional adn_stock_aging / shelf-life extensions | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-011 | Stock reservations | STD | Standard Odoo | adn_inventory_adjustment_approval; optional adn_stock_aging / shelf-life extensions | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-012 | Damaged stock segregation | CFG | Standard Odoo + configuration | adn_inventory_adjustment_approval; optional adn_stock_aging / shelf-life extensions | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-013 | Movement history | STD | Standard Odoo | adn_inventory_adjustment_approval; optional adn_stock_aging / shelf-life extensions | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-014 | Stock aging | CFG/CUS | Custom / configuration-dependent | Standard report first; optional stock aging extension (CUS-012) | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-INV-015 | Inventory valuation report | STD/CFG | Standard Odoo + configuration | adn_inventory_adjustment_approval; optional adn_stock_aging / shelf-life extensions | TC-INV-001–007 | Approved Baseline; execution pending |
| FSD-LOG-001 | Create delivery from sales order | STD | Standard Odoo | CUS-011 delivery discrepancy fields if standard capability insufficient | TC-LOG-001; delivery discrepancy and KPI reconciliation | Approved Baseline; execution pending |
| FSD-LOG-002 | Record planned and actual delivery dates | CFG/CUS | Custom / configuration-dependent | Standard delivery dates/reporting; conditional CUS-011 / CUS-008 | TC-LOG-001; delivery discrepancy and KPI reconciliation | Approved Baseline; execution pending |
| FSD-LOG-003 | Track dispatch status | CFG | Standard Odoo + configuration | CUS-011 delivery discrepancy fields if standard capability insufficient | TC-LOG-001; delivery discrepancy and KPI reconciliation | Approved Baseline; execution pending |
| FSD-LOG-004 | Capture POD document/reference | STD/CFG | Standard Odoo + configuration | CUS-011 delivery discrepancy fields if standard capability insufficient | TC-LOG-001; delivery discrepancy and KPI reconciliation | Approved Baseline; execution pending |
| FSD-LOG-005 | Record delivery discrepancy | CUS/CFG | Custom / configuration-dependent | CUS-011 delivery discrepancy extension (conditional) | TC-LOG-001; delivery discrepancy and KPI reconciliation | Approved Baseline; execution pending |
| FSD-LOG-006 | Report delivery performance | CFG/CUS | Custom / configuration-dependent | Standard delivery dates/reporting; conditional CUS-011 / CUS-008 | TC-LOG-001; delivery discrepancy and KPI reconciliation | Approved Baseline; execution pending |
| FSD-ACC-001 | Configure company accounting foundation | CFG | Standard Odoo + configuration | adn_credit_control and approval adapters only where specified | TC-ACC-001–002; financial reconciliation | Approved Baseline; execution pending |
| FSD-ACC-002 | Manage customer invoices and credit notes | STD | Standard Odoo | adn_credit_control and approval adapters only where specified | TC-ACC-001–002; financial reconciliation | Approved Baseline; execution pending |
| FSD-ACC-003 | Manage vendor bills and vendor credits | STD | Standard Odoo | adn_credit_control and approval adapters only where specified | TC-ACC-001–002; financial reconciliation | Approved Baseline; execution pending |
| FSD-ACC-004 | Manage AR/AP | STD/CFG | Standard Odoo + configuration | adn_credit_control and approval adapters only where specified | TC-ACC-001–002; financial reconciliation | Approved Baseline; execution pending |
| FSD-ACC-005 | Register payments | STD | Standard Odoo | adn_credit_control and approval adapters only where specified | TC-ACC-001–002; financial reconciliation | Approved Baseline; execution pending |
| FSD-ACC-006 | Reconcile payments and statements | STD | Standard Odoo | adn_credit_control and approval adapters only where specified | TC-ACC-001–002; financial reconciliation | Approved Baseline; execution pending |
| FSD-ACC-007 | Integrate inventory valuation | CFG | Standard Odoo + configuration | adn_credit_control and approval adapters only where specified | TC-ACC-001–002; financial reconciliation | Approved Baseline; execution pending |
| FSD-ACC-008 | Recognize COGS | CFG | Standard Odoo + configuration | adn_credit_control and approval adapters only where specified | TC-ACC-001–002; financial reconciliation | Approved Baseline; execution pending |
| FSD-ACC-009 | Validate PO/receipt/bill matching | CFG/CUS | Configuration + possible approved extension | adn_credit_control and approval adapters only where specified | TC-ACC-001–002; financial reconciliation | Approved Baseline; execution pending |
| FSD-ACC-010 | Produce financial statements | STD/CFG | Standard Odoo + configuration | adn_credit_control and approval adapters only where specified | TC-ACC-001–002; financial reconciliation | Approved Baseline; execution pending |

# 4. Supplemental Traceability for Narrative Functional Requirements
The following items capture material functional controls, workflow rules, data requirements, and acceptance obligations that are defined in FSD narrative sections but are not assigned a dedicated FSD-xxx-nnn identifier. `RTM-DER-*` is an RTM-only identifier. The originating FSD section is shown for auditability.

| RTM Derived ID | Derived Requirement / Control | Source Trace | Fit-Gap / Design Treatment | TDD Component | Verification / Evidence | Owner |
|---|---|---|---|---|---|---|
| RTM-DER-001 | Replenishment demand and minimum/maximum stock rules | FSD §6.6; BPM-005 | Odoo Inventory reordering rules, routes, vendor lead times | Configuration; no custom addon by default | Proposed: replenishment scenarios; min/max boundary tests (formal test IDs to be assigned in test pack) | Supply Chain / Operations |
| RTM-DER-002 | Inter-warehouse transfer across WH-JKT, WH-BDG and WH-SBY, including transit visibility | FSD §6.6; BPM-006 | Standard internal transfers, warehouse routes, transit locations | Configuration; transfer approval only if DEC-014 requires it | Multi-warehouse transfer E2E; in-transit and receipt reconciliation | Operations |
| RTM-DER-003 | Receiving workflow for full and partial receipts, discrepancy handling and putaway | FSD §6.8; BPM-008 | Standard purchase receipts, backorders, putaway rules | Configuration; CUS-011 only for approved discrepancy fields | TC-WH-001; receipt discrepancy and putaway tests | Warehouse / Procurement |
| RTM-DER-004 | Picking, packing, dispatch and backorder controls | FSD §6.8; BPM-009 | Standard delivery picking, packages, validation, backorders | Configuration; no custom addon unless approved | TC-WH-002; picking/packing/dispatch E2E | Warehouse |
| RTM-DER-005 | Incoming and outgoing quality inspection checklists | FSD §6.9; BPM-010 | Odoo Quality control points, checks, alerts and quarantine locations | Configuration first; CUS-010 conditional | TC-QUA-001/002; critical defect and disposition tests | Quality / Operations |
| RTM-DER-006 | Critical defects must hold affected lot/quantity pending disposition | FSD §6.9 | Quality alert/check plus stock quarantine and release authorization | Configuration; custom guard only if standard flow cannot enforce policy | Critical-defect negative test; release authorization test | Quality / Warehouse |
| RTM-DER-007 | Shelf-life eligibility and expiration severity thresholds | FSD §6.7, §6.15; FGA CUS-009 | Lot expiration dates, FEFO and eligibility validation | CUS-009 conditional; DEC-013 required for override | Expired/near-expiry boundary tests; customer minimum shelf-life test | Operations / Sales |
| RTM-DER-008 | Customer return physical receipt, inspection, disposition and restocking/scrap decision | FSD §6.11; BPM-012 | Standard return picking, quality disposition, stock locations | Standard + configuration; refund addon is separate | Return-to-stock, quarantine and scrap E2E | Customer Service / Warehouse |
| RTM-DER-009 | Supplier return linked to original receipt/vendor transaction | FSD §6.11; BPM-013 | Standard return transfer and vendor credit linkage | Standard + configuration | Supplier return E2E and inventory/AP reconciliation | Procurement / Finance |
| RTM-DER-010 | Refund financial execution must be controlled separately from physical return | FSD §6.11; FGA CUS-006; TDD §5.5 | Standard credit note/payment with ADN approval gate | adn_approval_core + adn_refund_approval; DEC-011 gate definition | TC-RET-001/002; credit-note posting/payment execution tests | Finance / Customer Service |
| RTM-DER-011 | Landed cost allocation to eligible imported receipts using approved cost components and allocation basis | FSD §6.13; BPM-015; FGA DEC-012 | Standard Landed Costs, valuation adjustment and accounting | Configuration; custom extension only if standard fails approved requirement | TC-LC-001; landed cost allocation and GL reconciliation | Finance / Procurement |
| RTM-DER-012 | Vendor KPI formulas, weighted score, classifications and insufficient-data behavior | FSD §6.14; FGA CUS-007 | Custom scorecard calculation over standard PO/receipt/quality sources | adn_vendor_scorecard | TC-VPM-001/002; formula and source drill-down tests | Procurement |
| RTM-DER-013 | Vendor scorecard monthly refresh, formula version and source lineage | FSD §6.14; TDD §5.6, §9 | Scheduled idempotent calculation with period snapshots | adn_vendor_scorecard + scheduled job | Re-run determinism; stale period; source lineage tests | Procurement / Technical |
| RTM-DER-014 | Consolidated inventory, sales, procurement, warehouse and financial dashboard catalogue | FSD §6.15; FGA CUS-008 | Standard list/pivot/graph and reporting; custom consolidated views if required | CUS-008 (Should), conditional after KPI reconciliation | TC-RPT-001/002; KPI-to-source reconciliation | Reporting Owner / Finance |
| RTM-DER-015 | Dashboard formulas, date basis, filter behavior, refresh timestamp and source drill-down | FSD §6.15; FGA DEC-009 | Governed KPI definitions and report configuration | TDD §11.4 KPI governance; custom reporting only where needed | Filter/date basis tests; source drill-down; reconciliation sign-off | Reporting Owner |
| RTM-DER-016 | Role-based access for business functions and warehouse scope | FSD §6.16; TDD §7 | Odoo groups, ACLs and record rules | adn_approval_core security groups plus standard role groups | TC-SEC-001; positive/negative ACL and record-rule matrix | ERP / Department Owners |
| RTM-DER-017 | Segregation of duties, requester/approver separation and self-approval prevention | FSD §6.16; FGA CUS-001; TDD §4, §7 | Server-side authorization and approval-engine validation | adn_approval_core; SoD enforcement | Self-approval, delegated approval and unauthorized RPC tests | ERP / Internal Control |
| RTM-DER-018 | Approval audit history including policy version, approver, decision, timestamp, comments and amendment history | FSD §5.3, §6.16; TDD §4, §10 | Immutable approval event history and linked source records | adn_approval_core models: policy/rule/request/step/item/event | Audit completeness, immutability and traceability tests | ERP / Audit |
| RTM-DER-019 | Master-data migration sequence, dependency validation and exception reporting | FSD §6.1, §6.17; BPM-001 | Controlled import templates, pre-validation, staged imports | Configuration/import utility; no separate master ledger | TC-MD-001/002; migration rehearsal and exception-log review | ERP / Data Migration |
| RTM-DER-020 | Opening stock, lot/serial, expiration and opening accounting/valuation reconciliation | FSD §6.17 | Standard inventory/accounting opening procedures with controlled cut-off | Configuration and migration work package | Migration sample accuracy; stock-to-GL reconciliation | Finance / Warehouse |
| RTM-DER-021 | End-to-end Procure-to-Pay traceability from demand/RFQ/PO through receipt, bill and payment | FSD §7.1; BPM-004 | Linked standard Odoo documents with custom PO approval gate | adn_purchase_approval + standard Odoo records | E2E-001; TC-PUR and TC-ACC suite | Procurement / Finance |
| RTM-DER-022 | End-to-end Order-to-Cash traceability from CRM/quotation through delivery, invoice and payment | FSD §7.2; BPM-003 | Linked CRM, Sales, Stock and Accounting documents | adn_sale_discount_approval + adn_credit_control | E2E-002; TC-CRM, TC-SAL, TC-CRD, TC-ACC | Sales / Finance |
| RTM-DER-023 | Multi-warehouse replenishment and transfer lifecycle | FSD §7.3; BPM-005/006 | Standard replenishment and internal transfer routes | Configuration; DEC-014 for approval policy | E2E-003; transfer stock reconciliation | Operations |
| RTM-DER-024 | Lot and expiration end-to-end traceability, FEFO selection and expired stock prevention | FSD §7.4; BPM-007/008/009 | Standard lots, expiration, FEFO, warehouse locations | Configuration; CUS-009 conditional | E2E-004; lot traceability and expiry boundary tests | Warehouse / Quality |
| RTM-DER-025 | Credit limit violation workflow including current exposure, hold and authorized exception release | FSD §7.5; FGA CUS-004; TDD §5.3 | Credit exposure service using posted AR and uninvoiced order commitments | adn_credit_control + approval engine | E2E-005; TC-CRD-001–004; concurrency and stale-snapshot tests | Finance / Sales |
| RTM-DER-026 | Supplier delivery discrepancy lifecycle and vendor performance impact | FSD §7.6; FGA CUS-011; DEC-015 | Receipt discrepancy evidence and scorecard source rules | CUS-011 conditional + adn_vendor_scorecard | E2E-006; discrepancy-to-scorecard reconciliation | Procurement / Warehouse |
| RTM-DER-027 | Customer return and refund E2E with separate physical and financial controls | FSD §7.7; FGA CUS-006; TDD §5.5 | Standard return and accounting records with approval execution gate | adn_refund_approval | E2E-007; TC-RET-001/002 | Customer Service / Finance |
| RTM-DER-028 | Imported goods and landed cost E2E including allocation and valuation impact | FSD §7.8; BPM-015 | Standard landed cost workflow and stock valuation | Configuration; DEC-012 | E2E-008; TC-LC-001 | Procurement / Finance |
| RTM-DER-029 | Inventory adjustment and cycle-count workflow including valuation approval | FSD §7.9; FGA CUS-005; TDD §5.4 | Standard inventory adjustment gated by reusable approval engine | adn_inventory_adjustment_approval | E2E-009; TC-INV-004–007; server-side bypass tests | Warehouse / Finance |
| RTM-DER-030 | Vendor performance period calculation and classification E2E | FSD §7.10; FGA CUS-007 | Scheduled vendor scorecard snapshots | adn_vendor_scorecard | E2E-010; TC-VPM-001/002 | Procurement |
| RTM-DER-031 | Non-functional performance target and response-time governance | FSD §9.1; FGA DEC-017; TDD §14 | Target-environment performance baseline and load test | Infrastructure/configuration plus code optimization as evidenced | Load/concurrency test; report p95 and workload profile | Technical Lead |
| RTM-DER-032 | Security hardening, unauthorized access prevention and auditability | FSD §9.2, §9.4; TDD §7, §10 | Least privilege, ACL/record rules, server-side guards and audit events | adn_approval_core + standard Odoo security | Security test suite; access matrix and audit inspection | Technical Lead / ERP Manager |
| RTM-DER-033 | Availability, backup, restore and recovery validation | FSD §9.3; TDD §14 | Infrastructure backup/restore runbooks and recovery test | Deployment/operations work package | Backup restore evidence; recovery test record | Infrastructure / ERP Manager |
| RTM-DER-034 | Data integrity, source transaction lineage and accounting reconciliation | FSD §9.4; TDD §6, §8, §10 | Standard transaction records, relational links, snapshots and immutable events | All custom addons; standard Odoo ledgers remain authoritative | Referential integrity, reconciliation and audit tests | Technical / Finance |
| RTM-DER-035 | Scalability and usability for baseline data volumes and operational users | FSD §9.5; TDD §3, §6 | Odoo configuration, indexes, batching, bounded jobs | Cross-module technical design | Volume, concurrency and usability tests | Technical Lead |
| RTM-DER-036 | Technical deployment, module installation order, upgrade and rollback readiness | TDD §13 | Version-controlled addons, staged release and rollback plan | All ADN addons and deployment pipeline | Install/upgrade/rollback evidence | Technical Lead / DevOps |

# 5. Fit-Gap Customization Traceability
This register preserves the approved FGA customization backlog identifiers and links each item to FSD requirements, TDD implementation, and verification. Conditional items remain conditional even though the design baseline is approved; approval of the document does not automatically authorize a Should-priority customization without its stated proof/decision.

| FGA ID | Capability | Priority | Primary FSD Trace | TDD Trace | Verification Focus | Build Disposition |
|---|---|---|---|---|---|---|
| CUS-001 | Reusable Approval Framework | Must | Approval requests, tiers, approvers, state, comments, history, re-submission | adn_approval_core (§4) | Server-side lock, self-approval prevention, amendment re-evaluation | Must build/design |
| CUS-002 | PO Approval Policy | Must | Untaxed PO total after line discounts; tier routing | adn_purchase_approval (§5.1) | Boundary tests, requester/approver separation | Must build/design |
| CUS-003 | Sales Discount Approval | Must | Per-line discount tier and approval status | adn_sale_discount_approval (§5.2) | Multi-line and amendment tests | Must build/design |
| CUS-004 | Credit Exposure and Hold | Must | Exposure calculation, warning, hold, exception release | adn_credit_control (§5.3) | Reconciliation to AR/orders; no double count | Must build/design |
| CUS-005 | Inventory Adjustment Approval | Must | Absolute valuation difference and approver tier | adn_inventory_adjustment_approval (§5.4) | Value boundary, aggregation, valuation test | Must build/design |
| CUS-006 | Refund Approval | Must | Refund tier and execution lock | adn_refund_approval (§5.5) | Credit note/refund accounting test | Must build/design |
| CUS-007 | Vendor Scorecard | Must | KPI calculation, weighted score, classification, insufficient-data state | adn_vendor_scorecard (§5.6) | Formula, period, sample, source drill-down tests | Must build/design |
| CUS-008 | Consolidated Management Dashboards | Should | Cross-domain KPI views and drill-down | Consolidated reporting extension (§11; conditional) | Formula and reconciliation sign-off | Conditional; prove standard/configuration insufficiency and close decisions |
| CUS-009 | Shelf-Life Validation | Should | Customer/order-specific minimum shelf-life check | Shelf-life validation extension (§5.7.1; conditional) | Expiry boundary and override tests | Conditional; prove standard/configuration insufficiency and close decisions |
| CUS-010 | Quality Sampling Extension | Should | Sample quantity calculation and checklist fields | Quality sampling extension (§5.7.2; conditional) | Sampling and critical defect tests | Conditional; prove standard/configuration insufficiency and close decisions |
| CUS-011 | Delivery Discrepancy Fields | Should | Reason, quantity, evidence, resolution | Delivery discrepancy extension (§5.7.3; conditional) | Delivery KPI reconciliation | Conditional; prove standard/configuration insufficiency and close decisions |
| CUS-012 | Stock Aging Enhancement | Should | Aging buckets based on approved receipt/valuation basis | Stock aging extension (§5.7.4; conditional) | Reconcile to stock source | Conditional; prove standard/configuration insufficiency and close decisions |

# 6. Technical Design Traceability
## 6.1 Architecture and Addon Mapping
| Technical Capability | TDD Reference | Primary Models / Standard Objects | Traceable Requirements |
|---|---|---|---|
| Shared approval framework | TDD §4 | `adn.approval.policy`, `adn.approval.rule`, `adn.approval.request`, `adn.approval.step`, `adn.approval.item`, `adn.approval.event` | CUS-001; FSD-SAL-003/004; FSD-PUR-006/007/008; FSD-INV-009; FSD-SEC; RTM-DER-017/018 |
| Purchase approval adapter | TDD §5.1 | Extension of `purchase.order`; approval request reference and fingerprint | CUS-002; FSD-PUR-006/007/008; TC-PUR-001–006 |
| Sales discount adapter | TDD §5.2 | Extension of `sale.order` and `sale.order.line`; line-level approval item | CUS-003; FSD-SAL-003/004; TC-SAL-002–005 |
| Credit control | TDD §5.3 | Partner credit attributes; `adn.credit.evaluation`; standard AR and sale orders | CUS-004; FSD-SAL-005; RTM-DER-025; TC-CRD-001–004 |
| Inventory adjustment approval | TDD §5.4 | Standard inventory adjustment/quant/count flow plus approval link | CUS-005; FSD-INV-009; RTM-DER-029; TC-INV-004–007 |
| Refund approval | TDD §5.5 | Standard `account.move` credit note and return picking links; refund request/approval link | CUS-006; RTM-DER-010/027; TC-RET-001/002 |
| Vendor scorecard | TDD §5.6 | `adn.vendor.scorecard.period`, `adn.vendor.scorecard.line`; standard PO/receipt/quality source references | CUS-007; RTM-DER-012/013/026/030; TC-VPM-001/002 |
| Optional supply-chain extensions | TDD §5.7 | Standard lot, quality, picking and stock aging source objects | CUS-009–CUS-012; RTM-DER-005/007/026 |
| Security and SoD | TDD §7 | Odoo users/groups/ACL/record rules; approval authorization guards | FSD-MD-007; FSD-SEC; RTM-DER-016/017/032 |
| Server-side workflow and transactional consistency | TDD §8 | Standard action hooks, source fingerprints, transaction-safe validation | All approval-controlled requirements; RTM-DER-018/025/029 |
| Automation and scheduled jobs | TDD §9 | Idempotent scheduled jobs, bounded batch processing, retry/logging | FSD-CRM-007; FSD-VPM; FSD-RPT; RTM-DER-013/015 |
| Audit and reporting | TDD §10–11 | Approval events, source links, KPI snapshots and drill-down | FSD-SEC; FSD-RPT; RTM-DER-013–018/032/034 |
| Deployment and operations | TDD §13–14 | Module manifests, release pipeline, upgrade/rollback, monitoring/runbooks | RTM-DER-031/033/035/036 |

## 6.2 Data Ownership and System-of-Record Traceability
| Data Domain | Authoritative System of Record | ADN Custom Layer | Integrity / Reconciliation Requirement |
|---|---|---|---|
| Sales orders and lines | Standard Odoo Sales | Approval state/reference and discount approval snapshot only | No parallel order ledger; approved amount/fingerprint must match source order |
| Purchase orders and lines | Standard Odoo Purchase | Approval state/reference and PO approval snapshot only | No parallel PO ledger; re-evaluate when approval-relevant values change |
| Stock quantities and movements | Standard Odoo Inventory | Approval gates and optional shelf-life/aging metadata | Stock moves/quants/valuation remain authoritative |
| Invoices, credit notes, payments, AR/AP | Standard Odoo Accounting | Approval reference/gate and evaluation snapshots | No duplicate receivable/payable ledger; reconcile to posted journal items |
| Customer credit policy | Approved partner credit attributes | Credit-limit approval and evaluation snapshots | Recalculate exposure from live accounting/order sources before release |
| Approval policies and decisions | ADN approval engine | Policy version, rules, request, steps, items, immutable events | Requester, approver, decision, timestamp, comments and source fingerprint auditable |
| Vendor scorecard | ADN derived reporting layer | Period snapshots, formula version and source lines | Deterministic calculation and drill-down to source PO/receipt/quality records |
| Quality checks | Standard Odoo Quality where configured | Optional sampling metadata only | Disposition must map to stock availability/quarantine and be auditable |

# 7. Approval Policy and Security Traceability
## 7.1 Approval Workflow Coverage
| Workflow | Trigger / Evaluation Basis | Technical Adapter | Mandatory Controls | Key Tests |
|---|---|---|---|---|
| Purchase Order | Untaxed PO total after line discounts; tier thresholds in approved FSD | `adn_purchase_approval` + shared engine | No confirmation while pending/rejected; requester cannot self-approve; amendment invalidates stale approval; server-side gate | TC-PUR-001–006; UI/import/RPC bypass tests |
| Sales Discount | Per sales order line against approved reference price | `adn_sale_discount_approval` + shared engine | Reason for exceptional pricing; per-line tier; all controlled lines approved before confirmation; re-evaluation on amendment | TC-SAL-002–005; mixed-tier and amendment tests |
| Credit Exception | Posted AR + eligible uninvoiced confirmed SO commitments; warning/hold thresholds | `adn_credit_control` + shared engine | No double counting; stale snapshot recheck; concurrent order safety; exception scope and expiry | TC-CRD-001–004; concurrency tests |
| Inventory Adjustment | Sum of absolute per-line valuation differences after company-currency rounding; grouped by company + warehouse + accounting date; snapshot at submission and revalidate before release; parallel all-required routing (DEC-003 closed 2026-11-22) | `adn_inventory_adjustment_approval` + shared engine | Standard apply/validate blocked while pending; count/fingerprint rechecked before execution; positive/negative lines do not offset; all required roles approve | TC-INV-004–012; aggregation, rounding, grouping, warehouse-mapping, valuation-staleness, role-separation, UI/import/RPC bypass tests |
| Customer Refund | Refund tier and execution point subject to DEC-011 | `adn_refund_approval` + shared engine | Physical return separate from financial refund; approval gate controls agreed credit-note/payment action | TC-RET-001/002; posting and payment execution tests |

## 7.2 Security and Segregation-of-Duties Controls
| Control ID | Control Requirement | TDD Trace | Verification Evidence |
|---|---|---|---|
| SEC-RTM-001 | Least-privilege group assignment; no ad hoc broad access | TDD §7.1–7.4 | Approved role-to-capability matrix; ACL/record-rule test results |
| SEC-RTM-002 | Requester cannot approve own transaction | TDD §7.5; approval engine | Self-approval negative tests for each approval adapter |
| SEC-RTM-003 | Approver can act only within assigned policy, company, amount/tier and authorization scope | TDD §4, §7 | Unauthorized approver and cross-scope tests |
| SEC-RTM-004 | Server-side enforcement applies to UI, import, RPC/API and automated execution | TDD §8.1 | Direct method/RPC/import bypass test evidence |
| SEC-RTM-005 | Record rules restrict operational data by role/company/warehouse where applicable | TDD §7.4 | Positive/negative record-rule matrix |
| SEC-RTM-006 | Approval decisions and events are auditable and not silently overwritten | TDD §4.2, §10.2 | Audit trail review and immutable event tests |
| SEC-RTM-007 | Credentials/secrets are not stored in plaintext migration files or logs | FSD §6.1; TDD §7.6 | Configuration/security inspection |

# 8. Decision and Dependency Traceability
Open FGA decisions remain governed dependencies and must be resolved before their respective build/release gates. DEC-003 is closed as of 2026-11-22; its approved implementation baseline and remaining runtime/UAT evidence are recorded below.

| Decision ID | Topic | Decision Owner | RTM Impact | Build / Test Gate |
|---|---|---|---|---|
| DEC-001 | Purchase Approval: Confirm approver routing, delegation, substitution, amendment behavior, and split-order monitoring | Procurement Manager | PO approval design and tests | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-002 | Sales Discount: Confirm discount reference price, rounding, cumulative discounts, line/order scope, reapproval | Sales Manager | Discount approval logic | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-003 | Inventory Adjustment: valuation cost; per-line currency rounding; sum of absolute line values; company + warehouse + accounting-date grouping; submission snapshot/release revalidation; parallel all-required approval | Operations + Finance | Adjustment approval logic | CLOSED — confirmed 2026-11-22; configuration, policy, tests, and module documentation updated. Runtime/UAT evidence remains a release gate. |
| DEC-004 | Costing: Validate FIFO/AVCO by category, automated valuation, accounts, and change restrictions | Finance Manager | Inventory valuation and migration | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-005 | Indonesian Tax: Confirm localization, tax mapping, rates, reporting, and professional review | Finance Manager | Accounting configuration | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-006 | Credit Management: Confirm exposure sources, order/invoice overlap, trigger, exception expiry, concurrent orders | Finance Manager | Credit calculation and hold | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-007 | Quality: Confirm checklist representation, sampling execution, defect severity, disposition authority | Operations / Quality | Quality configuration/customization | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-008 | Vendor Performance: Confirm date rules, due quantity logic, reference price, period cut-off, sample rule | Procurement Manager | Vendor scorecard | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-009 | Reporting: Confirm KPI date basis, model, refresh, reconciliation, audience, and filters | Reporting Owner | Dashboard design | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-010 | Data Migration: Confirm import templates, opening balances, historical transactions, cut-off | ERP Manager / Finance | Migration scope and rehearsal | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-011 | Refund Approval: Confirm gross/net basis, credit note vs cash refund, Finance review, execution point | Finance Manager | Refund workflow | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-012 | Landed Cost: Confirm eligible costs, allocation methods, already-sold quantities, period treatment | Finance Manager | Landed-cost configuration | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-013 | Shelf-Life Exception: Confirm who can override minimum remaining shelf life and with what evidence | Operations / Sales | Allocation validation | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-014 | Transfer Authority: Define when inter-warehouse transfers require approval and by what value/quantity | Operations Manager | Transfer workflow | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-015 | Delivery KPI: Define promised date, partial-delivery treatment, completion date, and discrepancy criteria | Operations Manager | Delivery dashboard | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-016 | Data Retention: Define retention and audit requirements for approval, POD, quality, and attachments | ERP Manager | Evidence design | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |
| DEC-017 | Performance Test: Define hardware, concurrency, dataset, and response measurement for 3-second target | Technical Lead | Infrastructure sizing | Close decision, record decision owner/date, update affected config and tests before implementation sign-off |

# 9. Test Traceability and Acceptance Evidence
## 9.1 Test Evidence Register
| Evidence ID | Required Evidence | Related Trace | Evidence Owner | Status at RTM Issue |
|---|---|---|---|---|
| EVD-001 | Approved requirement baseline and signed change log | All FSD requirements | Business Analyst / PMO | Pending evidence repository reference |
| EVD-002 | Odoo 19 environment validation report: installed apps, model/method hooks, localization, edition | FGA fit decisions; TDD §1.3 and §15 | Technical Lead | Pending |
| EVD-003 | Configuration workbook and screenshots/export of configured master data, warehouses, routes, rules | FSD-MD, PUR, INV, WH, ACC | Functional Lead | Pending |
| EVD-004 | Custom addon source review, manifest/dependency report and code-review approvals | CUS-001–CUS-012; TDD §2–8 | Technical Lead | Pending |
| EVD-005 | Automated unit/integration test reports including negative and bypass tests | FSD/TDD test catalogues | QA Lead | Pending |
| EVD-006 | End-to-end test scripts/results for E2E-001–E2E-010 | RTM-DER-021–030 | Process Owners / QA | Pending |
| EVD-007 | Security, ACL, record-rule and SoD test evidence | FSD-SEC; RTM-DER-016–018; SEC-RTM-001–007 | ERP Manager / QA | Pending |
| EVD-008 | Finance reconciliation: AR/AP/GL, stock valuation, COGS and landed cost | FSD-ACC, FSD-LC; RTM-DER-011/020/034 | Finance Manager | Pending |
| EVD-009 | Migration rehearsal, exception log, sample accuracy and opening reconciliation | FSD-MIG; RTM-DER-019/020 | Data Migration Lead | Pending |
| EVD-010 | Performance, concurrency, backup/restore, upgrade and rollback reports | RTM-DER-031/033/035/036 | Technical Lead / Infrastructure | Pending |
| EVD-011 | UAT sign-off and critical/high defect closure | SOW AC-001–AC-010; FSD §12 | Business Owners / PM | Pending |
| EVD-012 | Training, SOP, operational handover and support runbooks | FSD §10; TDD §14 | Project Manager / Operations | Pending |

## 9.2 SOW Acceptance Alignment
| SOW Acceptance ID | RTM Coverage | Minimum Evidence Required |
|---|---|---|
| AC-001 Scope Traceability | Sections 3–8; complete FSD requirement and derived control registers | Approved RTM with no unexplained orphan requirement |
| AC-002 Master Data Integrity | FSD-MD; RTM-DER-019/020 | Import validation, uniqueness, dependency and opening balance evidence |
| AC-003 Core Process Execution | FSD-CRM/SAL/PUR; RTM-DER-021/022 | E2E-001 and E2E-002 pass; source-to-downstream document links verified |
| AC-004 Inventory Control | FSD-INV; RTM-DER-001–007/023/024/029 | Warehouse, lot, expiry, FEFO, adjustment and valuation tests pass |
| AC-005 Financial Control | FSD-ACC/LC; RTM-DER-010/011/020/034 | AR/AP/GL, COGS, credit, refund and landed-cost reconciliation |
| AC-006 Quality and Supplier KPIs | FSD-QUA/VPM; RTM-DER-005/006/012/013/026/030 | Quality disposition and vendor scorecard formulas/source lineage pass |
| AC-007 Security | FSD-SEC; RTM-DER-016–018/032 | Role matrix, ACL, record rules, SoD and server-side bypass tests pass |
| AC-008 Technical Readiness | TDD architecture, modules, tests, deployment; RTM-DER-031/033/035/036 | Environment validation, code review, automated tests, performance and recovery evidence |
| AC-009 Operational Readiness | FSD process/E2E, SOP/training; EVD-011/012 | UAT sign-off, training completion, SOP and support handover |
| AC-010 Migration Quality | FSD-MIG; RTM-DER-019/020 | Migration rehearsal, exception closure and reconciliation signed off |

# 10. Non-Functional Requirements Traceability
| RTM-NFR ID | Requirement Area | Source | Technical Treatment | Verification |
|---|---|---|---|---|
| RTM-NFR-001 | Performance: response-time target and representative workload | FSD §9.1; FGA DEC-017; TDD §14 | Profile target hardware, query plans, indexes, bounded jobs and concurrency strategy | Baseline/load test; report p50/p95, workload and environment |
| RTM-NFR-002 | Security: least privilege and restricted data visibility | FSD §9.2; TDD §7 | Groups, ACLs, record rules, server-side authorization | Role matrix and negative access tests |
| RTM-NFR-003 | Availability and recovery | FSD §9.3; TDD §13–14 | Backup schedule, restore procedure, recovery runbook | Restore drill with timestamped evidence |
| RTM-NFR-004 | Data integrity and auditability | FSD §9.4; TDD §4/6/8/10 | Standard records, immutable approval events, fingerprints, transactional consistency | Integrity, audit and reconciliation tests |
| RTM-NFR-005 | Scalability and usability | FSD §9.5; TDD §3/6/9 | Indexes, batching, pagination, idempotent cron jobs | Volume test using agreed data set and operational walkthrough |
| RTM-NFR-006 | Maintainability and upgrade safety | TDD §2/13 | Modular addons, no core modification, manifests, migration scripts and rollback plan | Code review, install/upgrade/rollback test |
| RTM-NFR-007 | Observability and operational support | TDD §9/10/14 | Structured logs, job outcomes, actionable errors, monitoring signals and runbooks | Job failure/retry, alert and runbook exercise |

# 11. Orphan and Change Impact Management
## 11.1 Orphan Requirement Rules
A requirement is an orphan when it has no valid downstream mapping to a design/configuration item, verification method, or acceptance evidence. The RTM owner must run the following checks at each baseline/release review:
1. Every FSD requirement ID appears exactly once in Section 3 (unless an explicitly documented one-to-many decomposition is required).
2. Every CUS item in Section 5 maps to at least one FSD or derived requirement, a TDD component, and test evidence.
3. Every approval/security control maps to a server-side enforcement point and a negative/bypass test.
4. Every KPI maps to a formula, source model, date basis, refresh rule, access rule, and reconciliation evidence.
5. Every E2E scenario maps to process requirements and at least one execution script.
6. Every non-functional requirement maps to a measurable verification activity.

## 11.2 Change Impact Procedure
When an approved requirement, policy, threshold, data model, addon boundary, security rule, or Odoo version changes:
1. Register a change request with unique ID, reason, requester, impact, and target release.
2. Identify affected FSD IDs, RTM-DER IDs, CUS IDs, DEC IDs, TDD sections/models, tests, data migration scripts, reports, and SOPs.
3. Assess functional, technical, security, data, performance, operational, and commercial impacts.
4. Obtain approval from the relevant business owner, functional lead, technical lead, and project governance authority.
5. Update source baselines first where applicable, then update this RTM and linked artifacts under version control.
6. Re-run impacted regression and acceptance tests; retain old evidence and link superseding evidence.

# 12. Roles and RTM Governance
| Role | RTM Responsibility |
|---|---|
| Business Analyst / RTM Owner | Maintain IDs, descriptions, source references, bidirectional links, orphan checks and change history. |
| Functional Lead | Confirm FSD interpretation, standard/configuration/customization mapping and business acceptance criteria. |
| Technical Lead | Maintain TDD/addon/data/security mapping, technical feasibility and test hooks. |
| QA Lead | Maintain test coverage, execution results, defects, retests and evidence references. |
| Business Process Owner | Validate expected behavior, execute UAT and sign off acceptance evidence. |
| Project Manager / PMO | Control baselines, approvals, release gates, change requests and status reporting. |
| Finance / Internal Control | Approve accounting, valuation, credit, refund, audit and SoD evidence. |

# 13. Approval and Sign-Off
The baseline approval status of FSD, FGA and TDD is recorded as Approved per project instruction. This RTM itself requires controlled review and sign-off before it becomes the sole release-control register.

| Approval Role | Responsibility | Name | Status | Date / Reference |
|---|---|---|---|---|
| Project Sponsor / Managing Director | Business scope and priority approval | To be assigned | Pending RTM sign-off | To be recorded |
| Business Process Owners | Functional completeness and acceptance criteria | To be assigned | Pending RTM sign-off | To be recorded |
| ERP Functional Lead | FSD/FGA mapping and configuration classification | To be assigned | Pending RTM sign-off | To be recorded |
| ERP Technical Lead | TDD, module, data, security and workflow mapping | To be assigned | Pending RTM sign-off | To be recorded |
| QA Lead | Verification coverage and evidence governance | To be assigned | Pending RTM sign-off | To be recorded |
| ERP Project Manager | Baseline control and release governance | To be assigned | Pending RTM sign-off | To be recorded |

---
# Appendix A — Source Extraction and Completeness Notes
- FSD source file: `ADN_Functional_Specification_Document_v1.0.md` (2,169 lines); numbered requirement rows extracted: 72.
- FGA source file: `ADN_Fit_Gap_Analysis_v1.0.md`; CUS backlog and DEC register retained using original identifiers.
- TDD source file: `ADN_Technical_Design_Document_v1.0.md`; addon, data model, approval, security, workflow, test and deployment references are mapped to the RTM.
- Supplemental RTM-derived items are explicitly labeled and linked to source sections; they are not represented as newly approved FSD requirements.
- Where the FSD/FGA/TDD retain unresolved business decisions (DEC-001–DEC-017), this RTM preserves them as implementation gates rather than silently selecting a policy.

**End of Document — ADN-RTM-001 v1.0**
