# Scope of Work

## Advanced Wholesale Distribution & Supply Chain ERP Implementation

**PT Arunika Distribusi Nusantara | Odoo 19 Enterprise**

| Document Control | Value |
| --- | --- |
| Document ID | ADN-SOW-001 |
| Project ID | ADN-ERP-2026-001 |
| Version | 1.0 |
| Date | 16 November 2026 |
| Status | Draft -- Pending Portfolio Baseline Approval |
| BRD Reference | ADN-BRD-001, Version 1.1 -- Revised Draft, Pending Portfolio Baseline Approval |
| Classification | Portfolio / Fictional Business Case |
| Deployment | On-Premise / Ubuntu Linux / PostgreSQL |

> **Portfolio Disclaimer**
> PT Arunika Distribusi Nusantara, its stakeholders, policies, financial assumptions, users, and all datasets are fictional. This SOW is a portfolio implementation plan, not a commercial contract or evidence of an actual client engagement.

## Table of Contents

1. [Purpose and Objectives](#1-purpose-and-objectives)
2. [Project Reference and Design Principles](#2-project-reference-and-design-principles)
3. [Scope of Services](#3-scope-of-services)
4. [Delivery Phases and Work Packages](#4-delivery-phases-and-work-packages)
5. [Deliverables](#5-deliverables)
6. [Out of Scope](#6-out-of-scope)
7. [Technical and Solution Boundaries](#7-technical-and-solution-boundaries)
8. [Data Migration and Dataset Scope](#8-data-migration-and-dataset-scope)
9. [Roles and Responsibilities](#9-roles-and-responsibilities-raci-summary)
10. [Assumptions and Dependencies](#10-assumptions-and-dependencies)
11. [Acceptance Criteria](#11-acceptance-criteria)
12. [Quality, Testing and Evidence](#12-quality-testing-and-evidence)
13. [Change Control](#13-change-control)
14. [Risks and Mitigation](#14-risks-and-mitigation)
15. [Indicative Project Schedule](#15-indicative-project-schedule)
16. [Completion and Sign-Off](#16-completion-and-sign-off)
17. [BRD Traceability Summary](#17-brd-traceability-summary)
18. [Document Status and Governance](#18-document-status-and-governance)

# 1. Purpose and Objectives

- This Scope of Work (SOW) defines the implementation boundaries, work packages, deliverables, responsibilities, assumptions, dependencies, acceptance criteria, and change-control approach for the Odoo 19 Enterprise distribution ERP portfolio project. It is derived from BRD ADN-BRD-001 Version 1.1.

- Centralize sales, procurement, inventory, warehouse, accounting, and related distribution operations in one ERP platform.

- Establish standardized multi-warehouse processes across Jakarta, Bandung, and Surabaya.

- Improve product traceability through lot/serial tracking, expiration management, and FEFO allocation where applicable.

- Implement approval, credit, quality, vendor-performance, and reporting controls defined in the BRD.

- Demonstrate a controlled migration of fictional master data and opening datasets, with reconciliation evidence.

- Deliver a tested, documented, on-premise Odoo environment suitable for a professional implementation portfolio.

# 2. Project Reference and Design Principles

| Item | Baseline |
| --- | --- |
| Organization | PT Arunika Distribusi Nusantara (fictional B2B wholesale distributor) |
| Platform | Odoo 19 Enterprise |
| Hosting | On-premise deployment |
| OS / Database | Ubuntu Linux / PostgreSQL |
| Legal entity / currency | Single company / IDR |
| Scale | 500 products; 250 customers; 40 vendors; 3 warehouses; 30+ internal locations; 20 ERP users |
| BRD status | Revised Draft -- Pending Portfolio Baseline Approval |

The BRD defines business outcomes and policies; this SOW defines the delivery scope. Detailed screen behavior, model design, exact import mappings, technical architecture, and custom implementation decisions will be specified in the FSD, Fit-Gap Analysis, and TDD.

# 3. Scope of Services

## 3.1 In-Scope Functional Domains

| Scope ID | Domain | Included Services |
| --- | --- | --- |
| SCOPE-001 | Master Data Management | Configure product categories, UoMs, 500 products, 250 customers, 40 vendors, vendor product prices, customer pricelists, sales territories, warehouses, locations, and 20 user-role records. |
| SCOPE-002 | Sales Management | Configure quotations, sales orders, customer-specific pricelists, line discounts, sales team assignment, partial deliveries, backorders, invoicing flow, and sales history reporting. |
| SCOPE-003 | Customer Credit Management | Implement credit exposure calculation, 80% warning, 100% hold, overdue rules, credit exceptions, and auditable credit-limit changes. |
| SCOPE-004 | Purchase Management | Configure purchase requisitions subject to fit-gap, RFQs, multi-vendor quotation comparison, vendor price/lead-time records, PO approvals, partial receipts, and purchase history. |
| SCOPE-005 | Inventory Management | Configure multi-warehouse stock, internal locations, lot/serial tracking, expiration dates, FEFO allocation, category costing policy, inventory adjustments, cycle counting, and stock aging/valuation. |
| SCOPE-006 | Warehouse Operations | Configure incoming receipts, partial receipts, putaway, barcode-enabled operations where supported by licensed apps/devices, picking, packing, dispatch, and damaged/quarantine segregation. |
| SCOPE-007 | Supply Chain & Replenishment | Configure min/max and safety stock rules, forecast-based replenishment, vendor lead times, warehouse-specific replenishment, and replenishment reporting. |
| SCOPE-008 | Inter-Warehouse Transfers | Configure internal transfer routes and traceability between Jakarta, Bandung, and Surabaya, including partial dispatch/receipt and discrepancy handling. |
| SCOPE-009 | Quality Management | Configure incoming/outgoing quality checks, inspection sampling assumptions, pass/fail outcomes, defect severity, quarantine, and disposition traceability. |
| SCOPE-010 | Logistics & Delivery | Configure delivery orders, shipment status, proof-of-delivery capture/reference, delivery discrepancy recording, and delivery KPI source data. Full TMS/route optimization excluded. |
| SCOPE-011 | Returns & Reverse Logistics | Configure customer return requests, receipt/inspection/disposition, supplier returns, replacement/credit-note flow, and return reason reporting. |
| SCOPE-012 | Accounting & Financial Management | Configure chart of accounts/localization subject to validation, journals, receivables, payables, customer/vendor invoices, payments, reconciliation, perpetual inventory valuation, COGS, and financial reports. |
| SCOPE-013 | Landed Cost Management | Configure eligible landed cost types and allocation methods (weight, current cost, quantity) with accounting validation and traceable allocation. |
| SCOPE-014 | Vendor Performance Management | Implement monthly and rolling-three-month vendor KPIs, weighted scorecard, insufficient-data rule, source traceability, and purchase price variance display. |
| SCOPE-015 | Reporting, Security & Controls | Configure operational/financial dashboards, KPI definitions, role-based access, approval segregation, auditability, and least-privilege access. |

## 3.2 Cross-Functional End-to-End Scenarios

| Scenario | Name | Coverage |
| --- | --- | --- |
| E2E-001 | Procure to Pay | Replenishment → requisition → RFQ comparison → PO approval → receipt/quality → vendor bill matching → payment/reconciliation. |
| E2E-002 | Order to Cash | Quotation → pricing/discount → credit check → SO → reservation → pick/pack/delivery → invoice → receipt/reconciliation. |
| E2E-003 | Multi-Warehouse Replenishment | Shortage identification → transfer request/approval → dispatch → in-transit handling → destination receipt. |
| E2E-004 | Lot and Expiration | Lot capture → expiry alert → FEFO allocation → customer delivery traceability → recall simulation. |
| E2E-005 | Credit Limit Violation | Exposure calculation → warning/hold → exception approval → transaction release audit. |
| E2E-006 | Supplier Delivery Discrepancy | Partial receipt → quantity/quality discrepancy → quarantine/rejection → vendor KPI impact. |
| E2E-007 | Customer Return and Refund | Return request → authorization → receipt/inspection → stock disposition → credit note/refund approval. |
| E2E-008 | Imported Goods and Landed Costs | Import receipt → additional charges → allocation → valuation reconciliation. |
| E2E-009 | Inventory Adjustment and Cycle Counting | Count → variance valuation → approval tier → stock adjustment → accounting impact. |
| E2E-010 | Vendor Performance | Eligible receipts/inspections → KPI calculation → scorecard → drill-down to source records. |

# 4. Delivery Phases and Work Packages

| Phase | Work Package | Activities | Key Outputs |
| --- | --- | --- | --- |
| P1 | Initiation & Business Analysis | Confirm BRD baseline status; stakeholder walkthrough; clarify open decisions DEC-001--DEC-012; process mapping; fit-gap; project plan. | Approved project plan; process maps; decision log; fit-gap register. |
| P2 | Master Data Preparation | Generate/cleanse/validate 500 products, 250 customers, 40 vendors, 3 warehouses, 30+ locations, 20 users, UoM, categories, price lists, vendor prices. | Master data workbook; import templates; data validation log; data ownership sign-off simulation. |
| P3 | Core ERP Configuration | Company, localization baseline, accounting structure, sales, purchase, inventory, warehouses, payment terms, pricelists, taxes as illustrative only, user groups. | Configured core Odoo database; configuration workbook; screenshots/evidence. \|
| P4 | Advanced Warehouse & Supply Chain | Routes, putaway, replenishment, inter-warehouse flows, lot/serial, expiration, FEFO, barcode flows, quality checks, returns. | Warehouse/supply chain configuration; scenario evidence. |
| P5 | Financial Integration | AR/AP, invoice/payment flows, perpetual valuation, FIFO/AVCO category mapping, three-way match, credit exposure, landed cost, financial reports. | Accounting configuration; reconciliation workbook; finance test evidence. |
| P6 | Custom Development | Implement only approved gaps: purchase approval, discount approvals, inventory adjustment approvals, credit control, vendor scorecard, KPI/dashboard enhancements, refund approval, custom audit models as confirmed in FSD/TDD. | Custom addons source; technical documentation; unit tests; installation evidence. |
| P7 | Integration & Automation | Internal Odoo APIs/automated jobs and any explicitly approved integration endpoints; scheduled vendor KPI/dashboard refresh; logging and failure handling. | API/job specification; integration tests; operational logs. |
| P8 | Testing & UAT | Unit, integration, regression, security, migration, performance, backup/restore, E2E scenarios and user acceptance. | Test strategy/cases; execution results; defect log; UAT sign-off simulation. |
| P9 | Deployment & Handover | On-premise Ubuntu/PostgreSQL deployment, configuration hardening, backup/recovery, access handover, training, SOPs, go-live checklist and support handover. | Deployment guide; SOPs; training pack; handover checklist; final portfolio report. |

# 5. Deliverables

| ID | Deliverable | Description |
| --- | --- | --- |
| D-001 | Project initiation pack | Project plan, stakeholder/RACI, RAID and decision registers. |
| D-002 | Process & fit-gap pack | AS-IS/TO-BE maps, fit-gap analysis and approved solution approach. |
| D-003 | Master data pack | Workbook, import-ready staging files, data dictionary, validation and exception log. |
| D-004 | Configured Odoo baseline | Company, users, master data, sales, purchase, inventory, warehouse and accounting configuration. |
| D-005 | Functional design pack | FSDs for approvals, credit, quality, vendor KPIs, reporting, landed cost and returns. |
| D-006 | Technical solution pack | TDD, module architecture, API/job specs, security model and deployment topology. |
| D-007 | Custom addons | Source code, manifests, access rules, views, business logic, tests and installation instructions. |
| D-008 | Testing pack | Test strategy, test cases, test data, execution evidence, defect register and RTM. |
| D-009 | UAT pack | UAT scripts, business review records and clearly labeled simulated sign-off. |
| D-010 | Deployment & handover pack | Deployment/runbook, backup/restore proof, SOPs, training materials and handover checklist. |
| D-011 | Portfolio showcase pack | Architecture overview, process screenshots, key scenarios, KPI evidence and limitations. |

# 6. Out of Scope

- Manufacturing, MRP, production planning, HR, payroll, and employee lifecycle management.

- Full Transportation Management System, fleet maintenance, advanced route optimization, live vehicle tracking, and carrier marketplace integration.

- Customer-facing mobile application and direct integration with every Indonesian marketplace.

- AI-based demand forecasting, full customs brokerage integration, automated bank statement connections, and warehouse robotics.

- Real payment gateway, real bank connectivity, live carrier API, or third-party production integration unless separately approved by change request.

- Legal/tax advisory, statutory tax certification, and guarantee of compliance for a real company.

- Creation of genuine company identities, valid NPWP/NIK, real customer/vendor contact details, or actual signatures.

- Any capability not explicitly listed as in-scope is excluded unless accepted through formal change control.

# 7. Technical and Solution Boundaries

Target platform: Odoo 19 Enterprise, on-premise, Ubuntu Linux, PostgreSQL.

Use standard Odoo functionality and configuration wherever fit-gap confirms suitability; custom development is reserved for approved functional gaps.

Custom modules must follow Odoo module conventions, include manifest/dependencies, security access, views, business logic, tests, and technical documentation.

APIs are limited to approved system-to-system use cases; no external integration provider is assumed by this SOW.

Barcode capability depends on the selected Odoo apps, supported devices, and deployment configuration.

All imports must be repeatable in a controlled staging environment, with rejected-row logging and reconciliation.

Production-grade performance/security claims require tests in a defined infrastructure profile; the BRD's approximately 3-second form response is a test target, not a guarantee.

# 8. Data Migration and Dataset Scope

The portfolio data target follows BRD Section 7.2. This SOW explicitly separates master data from opening/transaction migration data.

| Dataset | BRD Target | SOW Treatment |
| --- | --- | --- |
| Products | 500 | Included master data dataset |
| Customers | 250 | Included master data dataset |
| Vendors | 40 | Included master data dataset |
| Warehouses | 3 | Included configuration master |
| Internal Locations | 30+ | Included; 11 locations per warehouse in this initial workbook |
| ERP Users | 20 | Included as fictional user-role staging records; actual logins/passwords must be provisioned securely in Odoo |
| Historical Sales Orders | 1,000 | Separate transaction dataset, not part of this master-data workbook |
| Historical Purchase Orders | 300 | Separate transaction dataset, not part of this master-data workbook |
| Opening Lots | 100 | Separate traceability/opening data set |
| Opening Stock Records | 500+ | Separate opening inventory dataset |
| Opening Customer Balances | ≤250 | Separate AR migration dataset |
| Opening Vendor Balances | ≤40 | Separate AP migration dataset |

Import dependency order: UoM and product categories → warehouses and locations → vendors/customers → products → vendor pricelists/customer pricelists → opening data.

All master identifiers must be unique; all foreign keys must reference existing records.

Tracked opening inventory must carry valid lot/serial identifiers; expiration-controlled products must carry valid expiration dates.

Opening stock quantity and valuation, AR, AP, and opening trial balance must reconcile before financial go-live simulation.

Historical transactions must remain clearly historical and must not be imported as open operational commitments unless explicitly required.

# 9. Roles and Responsibilities (RACI Summary)

| Role | RACI | Responsibility |
| --- | --- | --- |
| Project Sponsor / Managing Director | A | Executive direction; final portfolio baseline and scope decisions. |
| ERP Project Manager | A/R | Plan, coordinate, manage risks, scope, dependencies, change control and handover. |
| ERP Business Analyst | R | Requirements clarification, process mapping, FSD coordination and RTM. |
| Operations Manager | A/C | Warehouse, inventory, logistics, quality and operational acceptance. |
| Procurement Manager | A/C | Vendor, sourcing, purchasing, PO approval and vendor KPI acceptance. |
| Sales Manager | A/C | Customer, pricing, discount, sales and credit workflow review. |
| Finance Manager | A/C | Accounting, costing, tax assumptions, credit, landed cost and reconciliation. |
| ERP Technical Team | R | Environment, configuration, custom modules, APIs, testing and deployment. |
| Data Owners | R | Prepare and validate master/opening data; resolve data exceptions. |
| Key Users | R/C | Execute scenario testing, training review and UAT. |

R = Responsible; A = Accountable; C = Consulted. The names/roles are fictional portfolio roles. Actual responsibility assignment is a simulation.

# 10. Assumptions and Dependencies

## 10.1 Assumptions

One legal entity, IDR primary currency, B2B distribution model and three warehouses.

BRD policies and thresholds are treated as portfolio assumptions pending baseline approval and technical validation.

Odoo 19 Enterprise license and required applications are available for the project environment.

All company, user, customer, vendor, tax, and financial records are fictional.

Tax percentages in the BRD are illustrative test assumptions only and require professional/current regulatory validation before any real deployment.

Master data owners review and approve data quality before import.

## 10.2 Dependencies

Portfolio baseline review and approval of BRD v1.1.

Closure/validation of DEC-001 through DEC-012, especially workflow behavior and accounting impacts.

Availability of Odoo 19 Enterprise environment, Ubuntu host, PostgreSQL, backups and access credentials.

Approved user roles, warehouse SOPs, accounting policy, product tracking rules and test scenarios.

Prepared opening stock, opening balances and transaction history for migration phases beyond master data.

# 11. Acceptance Criteria

| Acceptance ID | Area | Acceptance Criteria |
| --- | --- | --- |
| AC-001 | Scope traceability | Every in-scope domain is mapped to BRD requirements, design artifacts and tests. |
| AC-002 | Master data integrity | 500 products, 250 customers, 40 vendors, 3 warehouses, at least 30 locations and 20 user records; unique IDs and valid references. |
| AC-003 | Core process execution | P2P and O2C complete successfully in the test environment. |
| AC-004 | Inventory control | Lot/serial, expiry, FEFO, warehouse transfers, adjustment approval and valuation are demonstrated for designated products. |
| AC-005 | Financial control | AR/AP, credit control, three-way matching, inventory valuation and landed cost reconcile to dummy control totals. |
| AC-006 | Quality and supplier KPIs | Inspection rules and vendor scorecard calculations reconcile to their source transactions. |
| AC-007 | Security | Role-based permissions and segregation of duties prevent unauthorized actions in test cases. |
| AC-008 | Technical readiness | Custom modules install; automated tests pass; API/jobs handle valid and invalid cases; backup/restore is demonstrated. |
| AC-009 | Operational readiness | SOPs and training material exist; key users complete assigned scenarios; zero open critical defects at simulated UAT sign-off. |
| AC-010 | Migration quality | MIG-001 to MIG-012 are evidenced; data migration accuracy target ≥99.5% on validated import sample. |

Acceptance is based on documented test evidence and reviewer confirmation. KPI targets are portfolio targets, not claims of achieved operational performance.

# 12. Quality, Testing and Evidence

- Unit testing for custom business logic and computed KPI calculations.

- Functional testing for each in-scope domain and approval threshold.

- Integration testing across P2P, O2C, warehouse, quality, accounting and returns.

- Migration testing with pre-import validation, rejected-row logs, post-import counts and reconciliation.

- Security testing for role access, approval segregation and record rules.

- Regression testing after changes to custom modules or core configuration.

- Performance testing under a documented dataset, hardware and concurrency profile.

- Backup and restore testing with documented recovery evidence.

- UAT execution using the ten BRD end-to-end scenarios.

# 13. Change Control

Any request that changes scope, deliverables, schedule, assumptions, data volumes, integrations, or acceptance criteria must be documented as a Change Request (CR). Each CR must include business reason, affected BRD/SOW IDs, functional/technical impact, effort and schedule impact, risks, alternatives, and approval. No out-of-scope work begins before the CR is accepted in the portfolio simulation.

# 14. Risks and Mitigation

| Risk ID | Risk | Mitigation |
| --- | --- | --- |
| RSK-001 | Poor master data quality | Unique keys, reference validation, owner review and import rehearsal. |
| RSK-002 | Opening stock/financial mismatch | Separate opening data preparation and reconciliation sign-off. |
| RSK-003 | Incorrect accounting/tax assumptions | Finance review; tax rates explicitly illustrative; validate before real use. |
| RSK-004 | Custom workflow defects | FSD/TDD, automated tests, approval matrix boundary tests and regression. |
| RSK-005 | Excessive customization | Fit-gap first; prefer standard Odoo; document justified gaps. |
| RSK-006 | Security/SoD gaps | Least privilege, role matrix, negative access tests and audit trail. |
| RSK-007 | Incorrect KPI results | Document formulas, date logic, source models and reconcile to raw records. |
| RSK-008 | Infrastructure/backup failure | Deployment checklist, monitored backup and restore rehearsal. |

# 15. Indicative Project Schedule

The schedule below is a planning baseline for the portfolio, not a contractual commitment. It assumes one implementation stream with staged review and timely stakeholder feedback.

| Period | Planned Activities |
| --- | --- |
| Weeks 1--2 | Initiation, BRD baseline review, decision closure, process mapping and fit-gap. |
| Weeks 3--4 | Master data preparation, cleansing, validation and import rehearsal. |
| Weeks 5--7 | Core Odoo configuration: company, sales, purchase, inventory, warehouse, users and accounting foundations. |
| Weeks 8--9 | Advanced warehouse, replenishment, transfers, quality, returns and landed cost. |
| Weeks 10--11 | Custom modules, credit controls, approval flows, vendor KPIs, dashboards and approved APIs/jobs. |
| Weeks 12--13 | System/integration/security/migration/performance tests and defect remediation. |
| Week 14 | UAT, user training, SOP completion and acceptance review. |
| Week 15 | Deployment rehearsal, backup/restore, handover and portfolio showcase. |

# 16. Completion and Sign-Off

The project work is considered complete for portfolio purposes when deliverables are submitted, acceptance criteria are evidenced, critical defects are closed, handover materials are available, and the simulated business owners review the results. No real stakeholder approval or signature is implied.

| Approver Role | Name (Fictional) | Decision | Date / Signature |
| --- | --- | --- | --- |
| Project Sponsor | Andika Pratama | Pending portfolio simulation | Not recorded \|
| Managing Director | Budi Santoso | Pending portfolio simulation | Not recorded \|
| Operations Manager | Rina Maharani | Pending portfolio simulation | Not recorded \|
| Procurement Manager | Dimas Saputra | Pending portfolio simulation | Not recorded |
| Sales Manager | Nadia Putri | Pending portfolio simulation | Not recorded |
| Finance Manager | Hendra Wijaya | Pending portfolio simulation | Not recorded \|
| ERP Project Manager | Fajar Nugraha | Pending portfolio simulation | Not recorded |

# 17. BRD Traceability Summary

| BRD Reference | Requirement Area | SOW Coverage |
| --- | --- | --- |
| BRD 5.1 | Master Data Management | SCOPE-001; P2; D-003 |
| BRD 5.2 | Sales & Credit | SCOPE-002/003; E2E-002/005 |
| BRD 5.3 | Purchase | SCOPE-004; E2E-001/006 |
| BRD 5.4--5.6 | Inventory, Warehouse, Supply Chain | SCOPE-005--008; E2E-003/004/009 |
| BRD 5.7--5.9 | Quality, Logistics, Returns | SCOPE-009--011; E2E-006/007 |
| BRD 5.10--5.11 | Accounting & Landed Cost | SCOPE-012/013; E2E-001/002/008 |
| BRD 5.12 | Vendor Performance | SCOPE-014; E2E-010 |
| BRD Reporting/Security | Dashboards & Access | SCOPE-015; AC-007/008 |
| BRD 7 | Data Migration | P2; D-003; AC-002/010 |
| BRD 8--13 | NFR, Roles, Risks, Acceptance | AC-001--010; P8/P9 |

# 18. Document Status and Governance

This SOW is Version 1.0 and remains a draft pending portfolio baseline approval. BRD ADN-BRD-001 Version 1.1 is also marked Revised Draft -- Pending Portfolio Baseline Approval. The SOW must be re-baselined if the BRD changes materially or if any open decision alters scope, cost, schedule, or acceptance.

END OF DOCUMENT
