# BUSINESS REQUIREMENTS DOCUMENT (BRD)
## Advanced Wholesale Distribution & Supply Chain ERP

**Project Name:** Advanced Wholesale Distribution & Supply Chain ERP Implementation  
**Company:** PT Arunika Distribusi Nusantara  
**ERP Platform:** Odoo 19 Enterprise  
**Deployment Model:** On-Premise  
**Operating System:** Ubuntu Linux  
**Database:** PostgreSQL  
**Document ID:** ADN-BRD-001  
**Project ID:** ADN-ERP-2026-001  
**Document Version:** 1.1  
**Document Status:** Approved  
**Prepared For:** ERP Implementation Case Study  
**Prepared By:** ERP Implementation Consultant  
**Document Date:** 16 November 2026  
**Classification:** Portfolio / Fictional Business Case

> **Portfolio Disclaimer:** PT Arunika Distribusi Nusantara, all stakeholder identities, operational policies, transaction values, financial figures, targets, and sample records in this document are fictional. They are designed as realistic assumptions for an ERP implementation portfolio. They do not represent an actual company's approved policies or official tax advice.

---

# DOCUMENT CONTROL

## 1. Document Information

| Attribute | Description |
|---|---|
| Project ID | ADN-ERP-2026-001 |
| Document ID | ADN-BRD-001 |
| Project Name | Advanced Wholesale Distribution & Supply Chain ERP |
| Organization | PT Arunika Distribusi Nusantara |
| ERP System | Odoo 19 Enterprise |
| Document Owner | ERP Business Analyst |
| Version | 1.1 |
| Status | Approved |
| Classification | Portfolio / Fictional Business Case |
| Currency | Indonesian Rupiah (IDR) |
| Country | Indonesia |

## 2. Revision History

| Version | Date | Description | Author |
|---|---|---|---|
| 1.0 | 12-Nov-2026 | Initial BRD preparation | ERP Business Analyst |
| 1.1 | 16-Nov-2026 | Clarified approval matrix, accounting policies, tax assumptions, credit management, quality criteria, vendor KPIs, dashboard formulas, and data migration requirements | ERP Business Analyst |

## 3. Approval Matrix

The following stakeholders represent fictional roles established for this portfolio case study.

| Role | Responsibility | Approval Status |
|---|---|---|
| Project Sponsor | Business direction, project objectives, and budget assumptions | Pending |
| Managing Director | Executive approval and business policy authorization | Pending |
| Operations Manager | Warehouse, inventory, logistics, and operational requirements | Pending |
| Procurement Manager | Purchasing, supplier selection, and vendor evaluation requirements | Pending |
| Sales Manager | Sales processes, pricing, discounts, and customer management | Pending |
| Finance Manager | Accounting, tax assumptions, credit control, and financial reporting | Pending |
| ERP Project Manager | Project coordination and requirements baseline control | Pending |

**Approval procedure:**

1. Each stakeholder reviews the requirements within their responsibility.
2. Questions and requested changes are recorded in the requirements review log.
3. The ERP Business Analyst updates the document where necessary.
4. The relevant stakeholder confirms the revised requirements.
5. The Project Sponsor and Managing Director provide final portfolio baseline approval.
6. The ERP Project Manager records the approved baseline version and date.

No stakeholder approval is claimed to have occurred merely because a fictional name or signature is included in this document. Approval must be represented as a clearly labeled portfolio simulation.

## 4. Document Usage and Baseline Rules

This BRD defines the business requirements and expected business outcomes. It does not prescribe the detailed Odoo implementation design.

The following document hierarchy applies:

| Document | Primary Purpose |
|---|---|
| BRD | Defines business needs, policies, requirements, and expected outcomes |
| SOW | Defines implementation scope, deliverables, responsibilities, and boundaries |
| Process Mapping | Defines AS-IS and TO-BE business processes |
| FSD | Defines detailed functional behavior and system requirements |
| Fit-Gap Analysis | Determines whether requirements use standard Odoo, configuration, customization, or integration |
| TDD | Defines technical architecture and custom development design |
| Test Strategy & Test Cases | Defines validation approach and test scenarios |
| RTM | Tracks requirements through design, implementation, and testing |

Any changes to an approved baseline must be recorded through a change request containing the requirement ID, reason, impact, priority, approval, and revised version.

---

# 1. EXECUTIVE SUMMARY

## 1.1 Business Overview

PT Arunika Distribusi Nusantara is a fictional Indonesian wholesale distribution company specializing in FMCG, household products, and consumer goods.

The company operates a Business-to-Business (B2B) distribution model, supplying:

- Traditional retail stores.
- Minimarkets and independent supermarkets.
- Wholesale merchants.
- Regional distributors.
- Corporate customers.
- Food service and hospitality businesses.

The company purchases products from local manufacturers, national suppliers, and selected international vendors before distributing them through regional warehouses.

The business currently relies on fragmented operational tools, spreadsheets, manual approval procedures, and partially integrated applications. These limitations affect inventory accuracy, procurement planning, order fulfillment, financial control, and management reporting.

The company intends to implement Odoo 19 Enterprise as its centralized ERP platform.

The implementation will connect the following business areas:

1. Master Data Management.
2. Sales Management.
3. Purchase Management.
4. Inventory Management.
5. Warehouse Management.
6. Supply Chain and Replenishment.
7. Inter-Warehouse Transfers.
8. Quality Management.
9. Logistics and Delivery.
10. Returns and Reverse Logistics.
11. Accounting and Financial Management.
12. Credit Management.
13. Vendor Performance Management.
14. Reporting and Business Intelligence.
15. Security and Internal Control.

## 1.2 Project Vision

To establish a scalable, integrated, and data-driven distribution management environment that improves operational efficiency, inventory accuracy, financial visibility, supplier performance, and customer service.

## 1.3 Project Objectives

| ID | Objective | Expected Business Outcome |
|---|---|---|
| OBJ-001 | Centralize business operations | Unified ERP platform |
| OBJ-002 | Improve inventory accuracy | More reliable stock records |
| OBJ-003 | Optimize procurement | Better purchasing decisions |
| OBJ-004 | Improve warehouse efficiency | Faster picking and fulfillment |
| OBJ-005 | Improve order management | Reduced order processing delays |
| OBJ-006 | Strengthen financial control | Accurate receivables and payables |
| OBJ-007 | Improve supplier management | Measurable vendor performance |
| OBJ-008 | Improve management visibility | Centralized operational reporting |
| OBJ-009 | Support business scalability | Standardized multi-warehouse processes |
| OBJ-010 | Improve product traceability | End-to-end lot and expiration tracking |

## 1.4 Expected Business Benefits

- Reduced manual data entry.
- Improved inventory visibility across warehouses.
- Reduced stock discrepancies.
- Better control of expired and near-expiration products.
- More accurate procurement planning.
- Improved supplier delivery performance.
- Faster sales order processing.
- Reduced order fulfillment delays.
- Improved customer credit management.
- More reliable financial reporting.
- Better management decision-making.

---

# 2. COMPANY PROFILE AND BUSINESS CONTEXT

## 2.1 Company Information

| Attribute | Dummy Information |
|---|---|
| Company Name | PT Arunika Distribusi Nusantara |
| Business Type | Wholesale Distribution |
| Industry | FMCG and Consumer Goods |
| Legal Structure | Limited Liability Company (PT) |
| Country | Indonesia |
| Head Office | Jakarta, Indonesia |
| Currency | IDR |
| Fiscal Year | January – December |
| Business Model | B2B Distribution |
| Number of Employees | 85 |
| Active Customers | 250 |
| Active Suppliers | 40 |
| Product Catalog | 500 SKUs |
| Distribution Warehouses | 3 |
| Sales Territories | 5 |

## 2.2 Business Locations

| Warehouse ID | Warehouse Name | Location | Primary Function |
|---|---|---|---|
| WH-JKT | Jakarta Central Warehouse | Jakarta | Main distribution center |
| WH-BDG | Bandung Regional Warehouse | Bandung | West Java distribution |
| WH-SBY | Surabaya Regional Warehouse | Surabaya | East Java distribution |

### Warehouse Responsibilities

**Jakarta Central Warehouse**

- Main supplier receiving point.
- Primary import receiving facility.
- Central inventory storage.
- Stock allocation to regional warehouses.
- National distribution coordination.

**Bandung Regional Warehouse**

- Regional order fulfillment.
- Customer distribution in West Java.
- Local stock replenishment.
- Regional inventory management.

**Surabaya Regional Warehouse**

- Regional order fulfillment.
- East Java customer distribution.
- Regional stock replenishment.
- Local inventory control.

## 2.3 Sales Territories

| Territory ID | Territory | Coverage |
|---|---|---|
| TERR-001 | Greater Jakarta | Jakarta, Bogor, Depok, Tangerang, Bekasi |
| TERR-002 | West Java | Bandung, Cirebon, Tasikmalaya |
| TERR-003 | Central Java | Semarang, Solo, Yogyakarta |
| TERR-004 | East Java | Surabaya, Malang, Kediri |
| TERR-005 | National Accounts | Strategic corporate customers |

## 2.4 Organizational Structure

| Department | Primary Responsibilities |
|---|---|
| Executive Management | Business strategy and corporate oversight |
| Sales Department | Customer acquisition and order management |
| Procurement Department | Supplier sourcing and purchasing |
| Warehouse Department | Receiving, storage, picking, and dispatch |
| Logistics Department | Delivery coordination |
| Inventory Control | Stock monitoring and reconciliation |
| Finance & Accounting | Invoicing, payments, and financial reporting |
| Customer Service | Customer inquiries and complaints |
| IT Department | ERP administration and technical support |

## 2.5 Business Operating Model

The company's primary operating cycle is:

1. Demand identification.
2. Inventory availability assessment.
3. Procurement planning.
4. Supplier quotation and selection.
5. Purchase order creation and approval.
6. Goods receiving.
7. Quantity and quality verification.
8. Inventory storage.
9. Customer order creation.
10. Stock reservation.
11. Picking and packing.
12. Delivery and shipment.
13. Customer invoicing.
14. Payment collection.
15. Financial reconciliation.
16. Management reporting.

---

# 3. CURRENT BUSINESS CHALLENGES

## 3.1 Existing Operational Environment

The fictional company currently uses:

- Microsoft Excel for inventory records.
- Spreadsheet-based purchasing plans.
- Manual sales order processing.
- Separate accounting applications.
- Manual warehouse stock reconciliation.
- Email and messaging applications for supplier communication.
- Manually prepared operational reports.

## 3.2 Identified Business Problems

| ID | Business Area | Existing Problem | Business Impact |
|---|---|---|---|
| CH-001 | Inventory | Inconsistent stock records | Inventory discrepancies |
| CH-002 | Procurement | Manual replenishment planning | Overstocking and stockouts |
| CH-003 | Warehouse | Limited stock location visibility | Inefficient picking |
| CH-004 | Sales | Manual stock confirmation | Delayed order processing |
| CH-005 | Expiration | Limited expiration monitoring | Product expiry losses |
| CH-006 | Purchasing | Inconsistent vendor evaluation | Poor supplier decisions |
| CH-007 | Logistics | Manual delivery coordination | Delayed shipments |
| CH-008 | Finance | Separate operational and financial records | Reconciliation difficulties |
| CH-009 | Reporting | Manual report preparation | Delayed management decisions |
| CH-010 | Multi-Warehouse | Limited cross-warehouse visibility | Unbalanced stock distribution |
| CH-011 | Credit Management | Manual customer credit monitoring | Higher collection risk |
| CH-012 | Returns | Inconsistent return documentation | Difficult inventory reconciliation |

## 3.3 Root Cause Analysis

1. Lack of centralized business data.
2. No standardized operational workflows.
3. Limited system-based internal controls.
4. Manual approval procedures.
5. Inconsistent master data.
6. Limited automation between departments.
7. Lack of real-time reporting.
8. Limited traceability between operational documents.

## 3.4 Business Transformation Requirements

The ERP implementation must address these challenges through standardized processes, centralized information, automated controls, and reliable reporting.

---

# 4. PROJECT SCOPE

## 4.1 In-Scope Business Areas

| No. | Business Domain | Scope |
|---|---|---|
| 1 | Master Data Management | Products, customers, suppliers, and locations |
| 2 | Sales Management | Quotations, sales orders, delivery, and invoicing |
| 3 | Purchase Management | RFQ, vendor selection, and purchase orders |
| 4 | Inventory Management | Stock movement, adjustment, and traceability |
| 5 | Warehouse Management | Receiving, putaway, picking, and packing |
| 6 | Supply Chain | Replenishment and stock planning |
| 7 | Inter-Warehouse Transfers | Internal stock distribution |
| 8 | Quality Management | Incoming and outgoing product inspections |
| 9 | Logistics | Shipment and delivery coordination |
| 10 | Returns Management | Customer and supplier returns |
| 11 | Accounting | Receivables, payables, and financial reporting |
| 12 | Credit Management | Customer credit limits and overdue monitoring |
| 13 | Vendor Management | Supplier performance evaluation |
| 14 | Reporting | Operational and financial dashboards |
| 15 | Security | User roles and access control |

## 4.2 Out-of-Scope Business Areas

The following processes are excluded from the initial implementation:

- Manufacturing and production planning.
- Human Resources and payroll.
- Full Transportation Management System (TMS).
- Fleet maintenance management.
- Customer-facing mobile application development.
- Direct integration with every Indonesian marketplace.
- Advanced AI-based demand forecasting.
- Full customs brokerage integration.
- Automated bank statement connections.
- Advanced warehouse robotics integration.

## 4.3 Implementation Approach

| Phase | Description |
|---|---|
| Phase 1 | Business analysis and requirements |
| Phase 2 | Master data preparation |
| Phase 3 | Core ERP configuration |
| Phase 4 | Advanced warehouse and supply chain implementation |
| Phase 5 | Financial integration |
| Phase 6 | Custom module development |
| Phase 7 | Integration and automation |
| Phase 8 | Testing and UAT |
| Phase 9 | Deployment and operational handover |

---

# 5. BUSINESS PROCESS REQUIREMENTS

# 5.1 MASTER DATA MANAGEMENT

## 5.1.1 Business Objective

Establish a centralized and standardized master data repository to ensure consistency across all operational departments.

## 5.1.2 Product Master Management

### Product Categories

| Category ID | Category | Example Products |
|---|---|---|
| CAT-001 | Food & Beverage | Packaged drinks, snacks |
| CAT-002 | Household Cleaning | Detergent, floor cleaner |
| CAT-003 | Personal Care | Soap, shampoo |
| CAT-004 | Kitchen Supplies | Tissue, kitchen accessories |
| CAT-005 | Consumer Goods | General household products |

### Sample Product Master Data

| Product Code | Product Name | Category | UoM | Tracking |
|---|---|---|---|---|
| SKU-0001 | Arunika Mineral Water 600ml | Food & Beverage | Unit | Lot |
| SKU-0002 | Arunika Cooking Oil 1L | Food & Beverage | Unit | Lot |
| SKU-0003 | FreshClean Detergent 800g | Household Cleaning | Unit | Lot |
| SKU-0004 | PureCare Shampoo 350ml | Personal Care | Unit | Lot |
| SKU-0005 | HomePlus Tissue 250 Sheets | Kitchen Supplies | Pack | None |
| SKU-0006 | Industrial Water Pump IP-100 | Consumer Goods | Unit | Serial |

### Business Requirements

- Unique internal product references.
- Product categorization.
- Multiple units of measure where applicable.
- Barcode identification.
- Sales and purchase pricing.
- Vendor-specific purchasing information.
- Lot and serial tracking for designated products.
- Expiration date tracking for applicable products.
- Reordering rules.
- Historical transaction preservation after product archival.

## 5.1.3 Customer Master Management

### Sample Customer Data

| Customer ID | Customer Name | Customer Type | Payment Terms | Credit Limit |
|---|---|---|---|---:|
| CUST-001 | PT Retail Makmur | Supermarket | Net 30 | IDR 100,000,000 |
| CUST-002 | CV Sumber Niaga | Wholesaler | Net 14 | IDR 50,000,000 |
| CUST-003 | Toko Berkah Jaya | Retail Store | Immediate | IDR 10,000,000 |
| CUST-004 | PT Sentosa Abadi | Corporate | Net 45 | IDR 150,000,000 |
| CUST-005 | UD Mitra Sejahtera | Retail Store | Net 7 | IDR 20,000,000 |

### Business Requirements

- Unique customer reference.
- Contact and address information.
- Payment terms.
- Individual credit limits.
- Assigned sales representatives.
- Designated delivery addresses.
- Tax identification information.
- Customer type classification.
- Traceable customer transactions.

## 5.1.4 Vendor Master Management

### Sample Vendor Data

| Vendor ID | Vendor Name | Vendor Type | Payment Terms | Country |
|---|---|---|---|---|
| VEND-001 | PT Nusantara Food Supply | Local Manufacturer | Net 30 | Indonesia |
| VEND-002 | PT Bersih Sejahtera | Local Manufacturer | Net 45 | Indonesia |
| VEND-003 | PT Global Consumer Goods | Distributor | Net 30 | Indonesia |
| VEND-004 | Shenzhen Trading Co. | International Supplier | Net 60 | China |
| VEND-005 | PT Prima Packaging | Local Supplier | Net 14 | Indonesia |

### Business Requirements

- Unique vendor reference.
- Supplier product and purchase price records.
- Vendor lead times.
- Supplier payment terms.
- Delivery performance measurement.
- Quality performance records.
- Multiple vendors per product.
- Historical purchasing information.

## 5.1.5 Warehouse and Location Master

### Sample Jakarta Warehouse Structure

- WH-JKT/Stock
- WH-JKT/Stock/Zone-A
- WH-JKT/Stock/Zone-B
- WH-JKT/Stock/Zone-C
- WH-JKT/Input
- WH-JKT/Quality
- WH-JKT/Packing
- WH-JKT/Output
- WH-JKT/Damaged
- WH-JKT/Returns

Equivalent location structures will be established for Bandung and Surabaya.

### Business Requirements

- Multiple warehouses.
- Hierarchical internal locations.
- Barcode operations.
- Product-specific storage restrictions.
- Quarantine and damaged stock segregation.
- Traceable source and destination inventory movements.

---

# 5.2 SALES MANAGEMENT

## 5.2.1 Business Objective

Establish a standardized sales process from quotation creation through order fulfillment, invoicing, and payment collection.

## 5.2.2 Sales Business Model

Supported order types:

1. Standard sales orders.
2. Contract-based sales.
3. Wholesale bulk orders.
4. Repeat customer orders.
5. Backorders.
6. Partial deliveries.
7. Customer returns.

## 5.2.3 Sales Process Flow

1. Customer submits a purchase request.
2. Sales representative creates a quotation.
3. Product availability is checked.
4. Pricing and discounts are reviewed.
5. Credit exposure is evaluated.
6. Customer confirms the quotation.
7. Sales order is confirmed.
8. Inventory is reserved.
9. Warehouse receives the delivery request.
10. Warehouse performs picking and packing.
11. Goods are dispatched.
12. Delivery is validated.
13. Customer invoice is generated.
14. Payment is received.
15. Outstanding receivables are reconciled.

## 5.2.4 Business Requirements

| ID | Business Requirement | Priority |
|---|---|---|
| BR-SAL-001 | Support sales quotations | Must |
| BR-SAL-002 | Convert confirmed quotations into sales orders | Must |
| BR-SAL-003 | Support customer-specific pricing | Must |
| BR-SAL-004 | Support volume-based discounts | Must |
| BR-SAL-005 | Check product availability | Must |
| BR-SAL-006 | Reserve inventory for confirmed orders | Must |
| BR-SAL-007 | Support partial deliveries | Must |
| BR-SAL-008 | Support backorders | Must |
| BR-SAL-009 | Support sales returns | Must |
| BR-SAL-010 | Support multiple delivery addresses | Should |
| BR-SAL-011 | Support sales team assignments | Must |
| BR-SAL-012 | Maintain sales order history | Must |
| BR-SAL-013 | Support customer-specific payment terms | Must |
| BR-SAL-014 | Support sales performance reporting | Should |
| BR-SAL-015 | Support quotation expiration dates | Should |

## 5.2.5 Customer Credit Management

### A. Credit Policy

The company applies a credit limit to customers approved for credit transactions.

Credit exposure is calculated as:

**Credit Exposure = Posted Outstanding Receivables + Open Confirmed Sales Orders Not Yet Invoiced**

**Available Credit = Approved Credit Limit − Credit Exposure**

The following items are treated as follows:

| Item | Included in Credit Exposure? |
|---|---|
| Posted unpaid customer invoices | Yes |
| Partially paid invoices | Yes, remaining balance only |
| Open confirmed sales orders not yet invoiced | Yes |
| Draft quotations | No |
| Cancelled sales orders | No |
| Fully paid invoices | No |
| Unallocated customer credit notes | Not until reconciled or allocated |

The exposure calculation must avoid double-counting the same commercial transaction. Once an order is invoiced, the corresponding open order commitment must no longer be counted separately if the invoice receivable represents the same obligation.

### B. Credit Control Rules

| Rule ID | Condition | System Action |
|---|---|---|
| CR-001 | Exposure is below or equal to 80% of limit | Normal processing |
| CR-002 | Exposure exceeds 80% but does not exceed 100% | Warning to Sales Representative |
| CR-003 | Exposure exceeds 100% | Credit hold; approval required |
| CR-004 | Customer has an invoice overdue by more than 30 calendar days | Credit hold |
| CR-005 | Customer has an invoice overdue by 1–30 calendar days | Warning and Finance review |
| CR-006 | Customer is marked as blocked by Finance | No new credit order confirmation |

### C. Credit Exception Approval

| Condition | Approval Required |
|---|---|
| Exposure exceeds credit limit by up to IDR 25,000,000 | Finance Manager |
| Exposure exceeds credit limit by more than IDR 25,000,000 | Finance Manager and Managing Director |
| Customer overdue more than 30 days | Finance Manager |
| Customer credit limit change | Finance Manager; Managing Director for increases above IDR 100,000,000 |

An approval does not automatically increase the permanent credit limit. It authorizes only the specific transaction or exception unless a separate credit-limit amendment is approved.

### D. Example Calculation

Customer: PT Retail Makmur

| Description | Amount |
|---|---:|
| Credit Limit | IDR 100,000,000 |
| Posted Outstanding Receivables | IDR 55,000,000 |
| Open Confirmed Sales Orders | IDR 20,000,000 |
| Total Credit Exposure | IDR 75,000,000 |
| Available Credit | IDR 25,000,000 |
| Exposure Utilization | 75% |

A new order of IDR 30,000,000 would result in exposure of IDR 105,000,000. The order must be placed on credit hold and routed for the required exception approval.

### E. Credit Management Requirements

- Each eligible customer must have an approved credit limit.
- Credit exposure must be calculated from defined transaction sources.
- Credit utilization must be visible to authorized users.
- Overdue invoices must be monitored.
- Orders exceeding the credit limit must be blocked from normal confirmation.
- Credit exceptions must be recorded with approver, date, reason, and scope.
- Credit limit changes must be auditable.
- Finance must be able to release or block customers according to policy.

## 5.2.6 Pricing and Discount Management

### Customer Pricing Policy

| Customer Category | Pricing Policy |
|---|---|
| Retail Store | Standard pricing |
| Wholesaler | Volume-based discount |
| Supermarket | Contract pricing |
| Corporate Customer | Negotiated pricing |

### Sales Discount Approval Matrix

| Discount Range | Approval |
|---|---|
| 0%–5% | Sales Representative |
| Above 5%–10% | Sales Supervisor |
| Above 10%–15% | Sales Manager |
| Above 15% | Sales Manager and Managing Director |

Rules:

- Discount percentages are evaluated per sales order line.
- The highest applicable discount tier determines the required approval.
- Discounts must not be hidden through manual price changes.
- Exceptional pricing must include a reason.
- Historical pricing and approvals must remain traceable.
- The approval policy applies to the fictional portfolio scenario and must be validated in functional design.

---

# 5.3 PURCHASE MANAGEMENT

## 5.3.1 Business Objective

Establish a controlled procurement process that ensures products are purchased at competitive prices, in appropriate quantities, and within required delivery schedules.

## 5.3.2 Procurement Business Model

Procurement activities may be triggered by:

- Reorder rules.
- Forecasted demand.
- Confirmed customer orders.
- Safety stock requirements.
- Seasonal demand.
- Management purchasing decisions.

The company purchases from domestic and international suppliers.

## 5.3.3 Purchase Process Flow

1. Inventory levels are monitored.
2. Replenishment requirements are identified.
3. Purchase requisitions are created.
4. Procurement reviews purchase requirements.
5. Supplier quotations are requested.
6. Vendor prices and lead times are compared.
7. Preferred suppliers are selected.
8. Purchase orders are prepared.
9. Purchase approval is obtained.
10. Purchase orders are sent to suppliers.
11. Suppliers confirm delivery schedules.
12. Warehouse receives incoming goods.
13. Quantity and quality are inspected.
14. Goods are accepted or rejected.
15. Supplier invoices are received.
16. Three-way matching is performed.
17. Supplier payments are scheduled.

## 5.3.4 Business Requirements

| ID | Business Requirement | Priority |
|---|---|---|
| BR-PUR-001 | Support purchase requisitions | Must |
| BR-PUR-002 | Support RFQ creation | Must |
| BR-PUR-003 | Support multiple vendor quotations | Must |
| BR-PUR-004 | Compare vendor prices | Must |
| BR-PUR-005 | Maintain vendor lead times | Must |
| BR-PUR-006 | Support purchase approval workflows | Must |
| BR-PUR-007 | Support purchase order confirmation | Must |
| BR-PUR-008 | Support partial supplier deliveries | Must |
| BR-PUR-009 | Support purchase returns | Must |
| BR-PUR-010 | Maintain purchase history | Must |
| BR-PUR-011 | Support minimum order quantities | Should |
| BR-PUR-012 | Support vendor performance evaluation | Should |
| BR-PUR-013 | Support blanket purchase agreements | Could |
| BR-PUR-014 | Support supplier price lists | Must |

## 5.3.5 Purchase Approval Matrix

The approval value is based on the total purchase order value before tax, after line discounts, expressed in IDR.

| Purchase Order Value | Required Approval |
|---|---|
| IDR 0–10,000,000 | Procurement Supervisor |
| Above IDR 10,000,000–50,000,000 | Procurement Manager |
| Above IDR 50,000,000–150,000,000 | Operations Manager |
| Above IDR 150,000,000 | Managing Director |

### Approval Rules

1. The applicable approval tier is determined by the final purchase order value.
2. A purchase order cannot be confirmed before its required approval is completed.
3. A change in quantity, unit price, discount, or other value-affecting field must trigger re-evaluation.
4. If an amendment moves the order into a higher approval tier, the higher approver must approve it.
5. The requester cannot approve their own purchase order.
6. Cancelled purchase orders must retain their approval history.
7. Splitting purchase orders to avoid approval thresholds is prohibited.
8. Taxes and non-purchase ancillary costs are excluded from the approval threshold calculation unless explicitly included by a future policy change.

### Approval Examples

| PO Reference | PO Value | Approval Tier |
|---|---:|---|
| PO-2026-0001 | IDR 8,500,000 | Procurement Supervisor |
| PO-2026-0002 | IDR 32,000,000 | Procurement Manager |
| PO-2026-0003 | IDR 95,000,000 | Operations Manager |
| PO-2026-0004 | IDR 210,000,000 | Managing Director |

## 5.3.6 Procurement Example

| Description | Value |
|---|---:|
| Product | Arunika Mineral Water 600ml |
| Current Stock | 500 Units |
| Reorder Threshold | 1,000 Units |
| Forecasted Demand | 3,000 Units |
| Proposed Purchase Quantity | 5,000 Units |
| Preferred Vendor | PT Nusantara Food Supply |
| Purchase Unit Price | IDR 2,500 |
| Estimated Purchase Value | IDR 12,500,000 |
| Vendor Lead Time | 7 Days |

Expected result: The system identifies the replenishment requirement and routes the resulting purchase order to the Procurement Manager because its value is above IDR 10,000,000 and below or equal to IDR 50,000,000.

---

# 5.4 INVENTORY MANAGEMENT

## 5.4.1 Business Objective

Provide accurate, real-time inventory visibility across all warehouses and establish strong controls over stock movement, traceability, and inventory valuation.

## 5.4.2 Inventory Management Requirements

| ID | Business Requirement | Priority |
|---|---|---|
| BR-INV-001 | Maintain real-time inventory balances | Must |
| BR-INV-002 | Support multiple warehouses | Must |
| BR-INV-003 | Support hierarchical storage locations | Must |
| BR-INV-004 | Support lot tracking | Must |
| BR-INV-005 | Support serial number tracking | Must |
| BR-INV-006 | Support expiration date tracking | Must |
| BR-INV-007 | Support FEFO allocation | Must |
| BR-INV-008 | Support approved product-category costing methods | Must |
| BR-INV-009 | Support inventory adjustments | Must |
| BR-INV-010 | Support cycle counting | Must |
| BR-INV-011 | Support inventory reservations | Must |
| BR-INV-012 | Support damaged inventory segregation | Must |
| BR-INV-013 | Maintain inventory movement history | Must |
| BR-INV-014 | Support stock aging reports | Should |
| BR-INV-015 | Support inventory valuation reporting | Must |

## 5.4.3 Lot and Expiration Management

### Sample Data

| Product | Lot Number | Manufacturing Date | Expiration Date | Quantity |
|---|---|---|---|---:|
| Mineral Water 600ml | LOT-MW-001 | 01-Nov-2026 | 01-Nov-2027 | 2,000 |
| Cooking Oil 1L | LOT-CO-001 | 15-Oct-2026 | 15-Oct-2027 | 1,500 |
| Detergent 800g | LOT-DT-001 | 20-Oct-2026 | 20-Oct-2028 | 1,000 |

### Business Rules

- Tracked products must have valid lot or serial identification.
- Expiration dates must be recorded for designated products.
- Products approaching expiration must be identifiable.
- Expired goods must not be allocated for normal sales delivery.
- FEFO must be applied to eligible products.
- Lot information must remain traceable through inventory movements.
- Product recall must be supported through lot identification.

### Expiration Alert Policy

| Remaining Shelf Life | Status | Required Action |
|---|---|---|
| More than 90 days | Normal | Standard inventory management |
| 61–90 days | Attention | Include in expiration monitoring report |
| 31–60 days | Warning | Notify Inventory Controller and Sales Manager |
| 1–30 days | Critical | Restrict allocation according to product policy and require review |
| Expired | Blocked | Move or retain in quarantine; prohibit normal sales allocation |

The alert is calculated from the lot expiration date against the current system date.

The company must maintain a minimum remaining shelf-life requirement for selected customers. The initial dummy policy is **90 days remaining shelf life at dispatch** for designated products, unless a customer contract specifies a stricter requirement.

A product may be physically present in stock but unavailable for allocation because it is expired, quarantined, damaged, or below the required remaining shelf life.

## 5.4.4 Inventory Valuation and Costing Policy

The company uses perpetual inventory valuation for the portfolio scenario. Inventory movements must produce the relevant valuation and accounting effects according to the configured product category and accounting policy.

### Product Category Costing Matrix

| Product Category | Costing Method | Valuation Policy | Rationale |
|---|---|---|---|
| CAT-001 – Food & Beverage | FIFO | Automated | Supports cost-flow traceability for frequently replenished goods |
| CAT-002 – Household Cleaning | AVCO | Automated | Simplifies average acquisition cost management |
| CAT-003 – Personal Care | FIFO | Automated | Supports distinct receipt-cost layers |
| CAT-004 – Kitchen Supplies | AVCO | Automated | Suitable for standardized products with recurring purchases |
| CAT-005 – Consumer Goods | AVCO | Automated | Simplifies cost management for general consumer products |

**Important distinction:**

- FIFO and AVCO are financial inventory costing methods.
- FEFO is a physical stock allocation strategy based on expiration dates.
- FIFO physical removal and FEFO physical removal are not interchangeable.
- A product may use FIFO valuation while warehouse picking follows FEFO.

### Costing Policy Rules

1. Costing method is assigned at product category level.
2. A product inherits the valuation configuration of its category unless an approved exception is defined.
3. Changes to costing configuration require Finance Manager approval.
4. Costing changes must be evaluated for accounting and valuation impact before implementation.
5. Inventory adjustments must generate traceable valuation effects.
6. Landed costs must be included where eligible under the approved acquisition-cost policy.
7. The company will not change the costing method for an existing category without documenting the reason and impact.
8. Opening inventory values must be reconciled before the system is treated as financially operational.

## 5.4.5 Inventory Adjustment

### Example

| Description | Quantity |
|---|---:|
| System Quantity | 1,000 |
| Physical Quantity | 970 |
| Difference | -30 |

### Inventory Adjustment Approval Matrix

| Absolute Inventory Difference Value | Required Approval |
|---|---|
| Up to IDR 1,000,000 | Warehouse Supervisor |
| Above IDR 1,000,000–10,000,000 | Warehouse Manager |
| Above IDR 10,000,000–50,000,000 | Operations Manager and Finance Manager |
| Above IDR 50,000,000 | Managing Director and Finance Manager |

The difference value is calculated using the inventory valuation cost of the affected quantity, not the sales price.

### Workflow

1. Warehouse identifies the discrepancy.
2. Physical counting is recorded.
3. Inventory adjustment is prepared.
4. System calculates the quantity and estimated value difference.
5. Required supervisor or manager reviews the discrepancy.
6. Authorized personnel approve the adjustment.
7. Inventory balance is updated.
8. Financial impact is recorded where applicable.
9. The adjustment history is retained.

No user may approve their own adjustment.

---

# 5.5 WAREHOUSE MANAGEMENT

## 5.5.1 Business Objective

Improve warehouse efficiency through standardized receiving, storage, picking, packing, and dispatch processes.

## 5.5.2 Incoming Goods Receiving

### Business Process

1. Supplier delivers products.
2. Warehouse checks the purchase order.
3. Goods are unloaded.
4. Delivered quantities are verified.
5. Lot and expiration information is recorded.
6. Quality inspection is performed where required.
7. Accepted goods are moved to storage.
8. Rejected goods are moved to quarantine.
9. Goods receipt is validated.

### Business Requirements

- Incoming goods must be linked to purchase orders.
- Partial receipts must be supported.
- Quantity discrepancies must be recorded.
- Lot numbers must be captured for tracked products.
- Quality inspection must be supported.
- Rejected products must be segregated.
- Putaway rules must be configurable.
- Goods receipt documentation must be available.

## 5.5.3 Putaway Management

| Product Category | Preferred Location |
|---|---|
| Food & Beverage | Zone A |
| Household Cleaning | Zone B |
| Personal Care | Zone C |
| High-Value Goods | Secure Storage |
| Damaged Goods | Quarantine |

Location assignment must consider product category, storage requirements, capacity, compatibility, zone, and handling requirements.

## 5.5.4 Order Picking

- Picking operations must be generated from confirmed sales orders.
- Stock must be reserved according to availability.
- Lot selection must respect FEFO where applicable.
- Barcode scanning must be supported.
- Picking quantities must be verified.
- Short-picked quantities must be recorded.
- Partial deliveries must be supported.
- Picking operations must be traceable.

## 5.5.5 Packing and Dispatch

- Picked goods must be prepared for packing.
- Packing operations must be linked to delivery orders.
- Package identification must be supported.
- Dispatch confirmation must be recorded.
- Delivery documentation must be generated.
- Shipment tracking information must be recorded where available.

## 5.5.6 Warehouse Operational Scenarios

| Scenario | Description | Expected Result |
|---|---|---|
| WH-SCN-001 | Standard receiving of 1,000 units | Receipt recorded and stock updated |
| WH-SCN-002 | Partial receiving of 700 out of 1,000 units | Remaining 300 units stay outstanding |
| WH-SCN-003 | 20 of 500 units rejected | Rejected quantity segregated |
| WH-SCN-004 | Two lots with different expiry dates | Earliest eligible expiry prioritized |
| WH-SCN-005 | Customer orders 100 units, only 80 picked | Short pick and backorder recorded |
| WH-SCN-006 | 15 damaged units discovered | Damaged stock segregated |

---

# 5.6 SUPPLY CHAIN AND REPLENISHMENT MANAGEMENT

## 5.6.1 Business Objective

Establish a proactive replenishment process to maintain sufficient stock availability while minimizing unnecessary inventory investment.

## 5.6.2 Replenishment Strategy

The company will use:

1. Minimum and maximum stock rules.
2. Safety stock.
3. Historical demand analysis.
4. Vendor lead time.
5. Warehouse demand.
6. Seasonal demand considerations.
7. Inter-warehouse replenishment.

## 5.6.3 Reorder Rule Example

| Parameter | Value |
|---|---:|
| Product | Arunika Mineral Water 600ml |
| Warehouse | Jakarta |
| Minimum Stock | 1,000 Units |
| Maximum Stock | 5,000 Units |
| Current Forecasted Stock | 800 Units |
| Vendor Lead Time | 7 Days |
| Target Replenishment Quantity | 4,200 Units |

The replenishment proposal is based on forecasted stock and the target maximum quantity, subject to purchase constraints and vendor minimum order quantities.

**Portfolio calculation:**

Target replenishment quantity = Maximum stock − Forecasted stock

= 5,000 − 800

= 4,200 units.

This example assumes there are no additional purchase orders or incoming transfers that would change forecasted stock.

## 5.6.4 Inter-Warehouse Replenishment

### Example

| Description | Quantity |
|---|---:|
| Product | FreshClean Detergent 800g |
| Jakarta Available Stock | 5,000 |
| Bandung Available Stock | 300 |
| Bandung Minimum Stock | 1,000 |
| Proposed Transfer | 1,500 |

### Process

1. Bandung identifies stock shortage.
2. Replenishment requirement is generated.
3. Jakarta inventory is evaluated.
4. Transfer request is created.
5. Transfer is approved.
6. Jakarta prepares and dispatches goods.
7. Goods are transported.
8. Bandung receives goods.
9. Inventory balances are updated.

## 5.6.5 Business Requirements

- Replenishment configurable by warehouse.
- Minimum and maximum stock rules.
- Safety stock.
- Vendor lead-time consideration.
- Traceable inter-warehouse transfers.
- Partial transfer shipments.
- Transfer discrepancy recording.
- Replenishment reports.

---

# 5.7 QUALITY MANAGEMENT

## 5.7.1 Business Objective

Ensure that incoming and outgoing products comply with the company's defined quality requirements.

## 5.7.2 Inspection Policy

Quality inspection is required for designated products and categories. Inspection criteria must be measurable and recorded against the related receipt, delivery, product, and lot where applicable.

The initial portfolio policy applies mandatory incoming inspection to:

- Food & Beverage.
- Personal Care.
- Selected Household Cleaning products.
- High-value serialized goods.

Outgoing inspection is mandatory for:

- Lot-tracked products with customer-specific shelf-life requirements.
- High-value goods.
- Products with previous quality complaints.
- Orders selected for additional quality sampling.

## 5.7.3 Incoming Quality Inspection Checklist

| Check ID | Inspection Parameter | Acceptance Criteria | Result |
|---|---|---|---|
| IQ-001 | Product identity | Matches PO and product specification | Pass/Fail |
| IQ-002 | Quantity | Physical quantity matches recorded accepted quantity | Pass/Fail |
| IQ-003 | Packaging | No visible tears, leaks, deformation, or contamination | Pass/Fail |
| IQ-004 | Product appearance | No visible damage, contamination, or abnormal appearance | Pass/Fail |
| IQ-005 | Lot identification | Lot number is present and readable for tracked products | Pass/Fail |
| IQ-006 | Expiration date | Expiration date is present and valid | Pass/Fail |
| IQ-007 | Remaining shelf life | At least 90 days for designated products | Pass/Fail |
| IQ-008 | Serial identification | Serial number present and unique for serialized products | Pass/Fail |

### Sampling Assumption

For the portfolio scenario, the default incoming inspection sample size is:

- Deliveries up to 100 units: inspect at least 5 units.
- Deliveries of 101–1,000 units: inspect at least 10 units.
- Deliveries above 1,000 units: inspect at least 20 units.

The quantity verification and packaging checks apply to the full shipment where operationally possible. Sampling applies to detailed appearance and product-condition inspection.

Any critical defect discovered in the sample triggers a hold on the affected lot until the Quality Inspector determines the disposition.

## 5.7.4 Outgoing Quality Inspection Checklist

| Check ID | Inspection Parameter | Acceptance Criteria |
|---|---|---|
| OQ-001 | Product identity | Matches sales order |
| OQ-002 | Quantity | Matches picking and delivery quantity |
| OQ-003 | Lot selection | Valid and eligible lot |
| OQ-004 | Expiration date | Not expired |
| OQ-005 | Remaining shelf life | Meets applicable customer requirement |
| OQ-006 | Packaging condition | No visible damage or leakage |
| OQ-007 | Customer specification | All mandatory order-specific requirements met |

All mandatory outgoing inspection criteria must pass before dispatch for orders subject to inspection.

## 5.7.5 Defect Classification

| Severity | Example | Required Action |
|---|---|---|
| Critical | Expired product, contamination, incorrect product identity | Reject or quarantine affected goods |
| Major | Damaged packaging affecting product protection, missing lot identity | Hold and investigate |
| Minor | Cosmetic packaging defect without product impact | Record and obtain authorized disposition |

## 5.7.6 Quality Disposition Rules

| Inspection Result | Inventory Disposition |
|---|---|
| Pass | Release to available stock |
| Fail – Critical | Quarantine or reject |
| Fail – Major | Quarantine pending review |
| Fail – Minor | Release only after authorized disposition |
| Pending | Remain in quality inspection location |

A Quality Inspector cannot independently approve the commercial or financial write-off of rejected goods. Such decisions follow the relevant approval matrix.

## 5.7.7 Quality Requirements

| ID | Requirement |
|---|---|
| BR-QUA-001 | Support incoming quality inspections |
| BR-QUA-002 | Support outgoing quality inspections |
| BR-QUA-003 | Record inspection results |
| BR-QUA-004 | Support pass/fail decisions |
| BR-QUA-005 | Segregate rejected products |
| BR-QUA-006 | Link quality records to source documents |
| BR-QUA-007 | Report quality defects |
| BR-QUA-008 | Support defined inspection checklists |
| BR-QUA-009 | Record defect severity and disposition |
| BR-QUA-010 | Maintain inspector, date, and approval history |

---

# 5.8 LOGISTICS AND DELIVERY MANAGEMENT

## 5.8.1 Business Objective

Establish a controlled distribution process that ensures customer orders are delivered accurately and on schedule.

## 5.8.2 Delivery Process

1. Delivery order is generated.
2. Warehouse completes picking.
3. Packing is completed.
4. Shipment is prepared.
5. Delivery documentation is generated.
6. Goods are dispatched.
7. Customer receives products.
8. Proof of delivery is recorded.
9. Delivery status is updated.

## 5.8.3 Delivery Requirements

- Delivery orders linked to sales orders.
- Configurable delivery addresses.
- Partial shipments.
- Traceable delivery status.
- Proof of delivery.
- Delivery discrepancy documentation.
- Shipping cost recording.
- Customer delivery performance measurement.

## 5.8.4 Delivery Performance KPIs

| KPI | Definition |
|---|---|
| On-Time Delivery Rate | Percentage of eligible deliveries completed on or before promised delivery date |
| Order Fulfillment Rate | Percentage of ordered quantity delivered |
| Delivery Accuracy | Percentage of deliveries completed without product or quantity discrepancy |
| Average Delivery Lead Time | Average elapsed time from dispatch to delivery confirmation |
| Partial Delivery Rate | Percentage of orders requiring more than one shipment |
| Failed Delivery Rate | Percentage of dispatched deliveries that fail to reach the customer |

Advanced route optimization and vehicle tracking are excluded from the initial implementation.

---

# 5.9 RETURNS AND REVERSE LOGISTICS

## 5.9.1 Business Objective

Establish standardized processes for handling customer returns and supplier returns.

## 5.9.2 Customer Return Scenarios

- Damaged products.
- Incorrect products delivered.
- Expired products.
- Incorrect quantities.
- Customer complaints.
- Approved commercial returns.

## 5.9.3 Customer Return Process

1. Customer submits a return request.
2. Customer Service reviews the complaint.
3. Return authorization is approved.
4. Goods are received.
5. Returned products are inspected.
6. Products are classified.
7. Accepted goods are returned to available stock, quarantine, or damaged stock as appropriate.
8. Credit note or refund is processed.
9. Return case is closed.

## 5.9.4 Supplier Return Process

1. Defective or incorrect goods are identified.
2. Procurement reviews the issue.
3. Supplier return is authorized.
4. Goods are transferred to the supplier return area.
5. Return shipment is processed.
6. Supplier credit or replacement is recorded.
7. Transaction is reconciled.

## 5.9.5 Business Requirements

- Return requests documented.
- Return reasons categorized.
- Returns reference original transactions.
- Returned goods undergo inspection.
- Return quantities traceable.
- Credit notes supported.
- Supplier replacement goods traceable.
- Return performance reportable.

---

# 5.10 ACCOUNTING AND FINANCIAL MANAGEMENT

## 5.10.1 Business Objective

Integrate operational transactions with financial accounting to provide accurate and timely financial information.

## 5.10.2 Accounting Scope

The system must support:

- Customer invoicing.
- Vendor bill processing.
- Accounts receivable.
- Accounts payable.
- Customer payments.
- Supplier payments.
- Bank and cash transactions.
- Inventory valuation.
- Cost of Goods Sold.
- Tax management.
- Journal entries.
- Financial reporting.

## 5.10.3 Accounting Process Integration

### Sales to Accounting

1. Sales order is confirmed.
2. Delivery is validated.
3. Customer invoice is generated according to company invoicing policy.
4. Receivable is recorded.
5. Customer payment is received.
6. Payment reconciliation is completed.

### Purchase to Accounting

1. Purchase order is confirmed.
2. Goods receipt is validated.
3. Supplier invoice is received.
4. Purchase order, receipt, and invoice are matched.
5. Vendor bill is approved.
6. Supplier payment is processed.
7. Payment reconciliation is completed.

### Inventory to Accounting

1. Goods are received.
2. Inventory valuation is updated.
3. Goods are delivered.
4. Inventory valuation decreases.
5. Cost of Goods Sold is recognized according to the configured accounting policy.

## 5.10.4 Three-Way Matching Policy

The company requires matching between:

1. Purchase Order.
2. Goods Receipt.
3. Vendor Bill.

### Matching Tolerances

| Matching Dimension | Allowed Tolerance | Action if Exceeded |
|---|---:|---|
| Invoiced quantity | No more than received quantity | Hold for review |
| Unit price difference | 1% or IDR 50,000, whichever is lower | Finance review |
| Total invoice difference | 1% of matched PO value | Finance Manager approval |
| Unreceived quantity | No invoice matching beyond received quantity without exception | Hold for review |

For the portfolio baseline, vendor bills must not be approved automatically when invoiced quantity exceeds received quantity.

### Example

| Document | Quantity | Unit Price |
|---|---:|---:|
| Purchase Order | 1,000 | IDR 2,500 |
| Goods Receipt | 1,000 | IDR 2,500 |
| Vendor Bill | 1,000 | IDR 2,500 |

Expected result: The documents match and can proceed through the normal approval process.

A mismatch must create an exception record with its reason, amount, responsible reviewer, and resolution.

## 5.10.5 Indonesian Tax Configuration Assumptions

The company operates in Indonesia. The ERP must support configurable Indonesian tax handling.

### Portfolio Tax Configuration

The following values are illustrative configuration assumptions for testing only. They are not a representation of the applicable statutory tax rate or a tax determination for a real company.

| Tax Code | Description | Illustrative Rate | Application |
|---|---|---:|---|
| TAX-PPN-OUT | Output VAT / PPN | 11% | Standard taxable sales scenario |
| TAX-PPN-IN | Input VAT / PPN | 11% | Standard taxable purchase scenario |
| TAX-PPN-EXEMPT | Exempt / non-taxable scenario | 0% | Dummy exempt transaction |
| TAX-PPN-IMPORT | Import VAT scenario | 11% | Dummy import transaction |

### Tax Configuration Rules

1. Tax rates must be configurable rather than hard-coded in custom business logic.
2. Tax mapping must be assigned to the relevant products, customers, vendors, and transaction types.
3. Input and output taxes must be recorded separately.
4. Tax-inclusive and tax-exclusive pricing must be supported where required.
5. Tax invoice references must be recorded where applicable.
6. Tax calculations must be validated against the applicable rules before production use.
7. The Finance Manager is responsible for approving the portfolio tax configuration.
8. Any actual deployment must use rates, tax bases, exemptions, documentation, and accounting treatment validated by a qualified Indonesian tax professional and current regulations.

**Important:** The illustrative 11% value is selected to make the dummy scenarios executable and testable. It must not be treated as confirmation of the correct tax treatment for a real transaction in 2026.

## 5.10.6 Financial Reporting

The system must provide:

- Profit and Loss Statement.
- Balance Sheet.
- Cash Flow Statement.
- Accounts Receivable Aging.
- Accounts Payable Aging.
- General Ledger.
- Trial Balance.
- Inventory Valuation.
- Customer Sales Analysis.
- Vendor Purchase Analysis.

---

# 5.11 LANDED COST MANAGEMENT

## 5.11.1 Business Objective

Ensure that imported products reflect their eligible acquisition costs, including additional procurement and logistics expenses.

## 5.11.2 Landed Cost Components

- International freight.
- Insurance.
- Customs-related charges.
- Port handling.
- Customs brokerage.
- Domestic transportation.
- Other eligible acquisition costs.

## 5.11.3 Example Scenario

| Cost Component | Amount |
|---|---:|
| Product Purchase Value | IDR 100,000,000 |
| International Freight | IDR 8,000,000 |
| Insurance | IDR 1,000,000 |
| Customs and Import Charges | IDR 12,000,000 |
| Port Handling | IDR 2,000,000 |
| Domestic Transportation | IDR 3,000,000 |
| Total Acquisition Cost | IDR 126,000,000 |

## 5.11.4 Allocation Policy

| Cost Type | Default Allocation Method | Reason |
|---|---|---|
| International Freight | By weight | Reflects transportation cost driver |
| Insurance | By current cost | Reflects insured goods value |
| Customs-related charges | By current cost | Reflects declared goods value assumption |
| Port Handling | By quantity | Simplified dummy allocation |
| Domestic Transportation | By weight | Reflects distribution cost driver |

The allocation method is a portfolio assumption. Actual allocation must follow the nature of the charge and the company's approved accounting policy.

Landed costs must be allocated only to eligible inventory and must be auditable.

---

# 5.12 VENDOR PERFORMANCE MANAGEMENT

## 5.12.1 Business Objective

Provide measurable supplier evaluation to support procurement decisions.

## 5.12.2 KPI Definitions and Formulas

The vendor performance evaluation period is monthly, with a rolling three-month view available for management analysis.

| KPI | Formula | Data Source |
|---|---|---|
| On-Time Delivery Rate | On-time eligible receipts ÷ total eligible receipts × 100 | Purchase orders and validated receipts |
| Order Fulfillment Rate | Accepted quantity received ÷ quantity due in the evaluation period × 100 | Purchase order lines and receipts |
| Quality Acceptance Rate | Accepted quantity ÷ inspected quantity × 100 | Quality inspection records |
| Lead Time Reliability | Receipts within agreed lead-time tolerance ÷ eligible receipts × 100 | PO confirmation and receipt dates |
| Purchase Price Variance | (Actual unit price − reference unit price) ÷ reference unit price × 100 | Purchase order lines and vendor price history |

### KPI Measurement Rules

**On-Time Delivery**

- Promised date is the confirmed vendor delivery date recorded on the purchase order.
- Actual date is the date the goods are physically received and the receipt is validated.
- A receipt is on time when the actual receipt date is on or before the promised date.
- Each purchase order receipt is evaluated at receipt level.
- Cancelled orders are excluded.

**Order Fulfillment Rate**

- The denominator is the quantity due during the evaluation period.
- The numerator is the accepted quantity received against that due quantity.
- Rejected quantities do not count as accepted fulfillment.
- Outstanding quantities remain unfulfilled until received or formally cancelled.

**Quality Acceptance Rate**

- The numerator is the quantity accepted by Quality.
- The denominator is the quantity inspected.
- Items not inspected are excluded from this KPI and reported separately.

**Lead Time Reliability**

- Planned lead time is the confirmed number of calendar days between the PO confirmation date and promised receipt date.
- Actual lead time is the number of calendar days between PO confirmation and validated receipt.
- The receipt is considered within tolerance if actual lead time is no more than planned lead time plus one calendar day.

**Purchase Price Variance**

- Reference unit price is the latest approved reference price for the same product and purchase UoM at the start of the evaluation period.
- Negative variance means the purchase price is lower than the reference price.
- Positive variance means the purchase price is higher than the reference price.
- This KPI is an indicator, not a standalone vendor quality score.

## 5.12.3 Vendor Scorecard

For management comparison, the portfolio uses the following weighted score:

| KPI | Weight |
|---|---:|
| On-Time Delivery Rate | 30% |
| Order Fulfillment Rate | 25% |
| Quality Acceptance Rate | 30% |
| Lead Time Reliability | 15% |
| Total | 100% |

The Purchase Price Variance is displayed separately and is not included in the weighted score to avoid treating a low price as automatically equivalent to better supplier performance.

**Vendor Score = (OTD × 30%) + (Fulfillment × 25%) + (Quality Acceptance × 30%) + (Lead Time Reliability × 15%)**

### Performance Classification

| Score | Classification |
|---|---|
| 95%–100% | Excellent |
| 90%–94.99% | Good |
| 80%–89.99% | Needs Improvement |
| Below 80% | Poor |

A vendor with fewer than five eligible receipts in the evaluation period must be marked **Insufficient Data** rather than being assigned a definitive performance classification.

## 5.12.4 Example Vendor Evaluation

| KPI | Target | Actual |
|---|---:|---:|
| On-Time Delivery | 95% | 92% |
| Order Fulfillment | 98% | 97% |
| Quality Acceptance | 99% | 98% |
| Lead Time Reliability | 95% | 94% |

Illustrative weighted score:

= (92% × 30%) + (97% × 25%) + (98% × 30%) + (94% × 15%)

= 27.60% + 24.25% + 29.40% + 14.10%

= **95.35% – Excellent**

The result is a dummy example, not a real supplier performance result.

## 5.12.5 Business Requirements

- Vendor performance must be calculated from historical transactions.
- KPI definitions must be consistent.
- Users must be able to filter by vendor and evaluation period.
- Insufficient data must be clearly identified.
- KPI calculations must be traceable to source records.
- Procurement must be able to review the underlying transactions.
- Manual changes to calculated KPI results must be restricted and audited.

---

# 5.13 CUSTOMER RELATIONSHIP MANAGEMENT

## 5.13.1 Business Objective

Improve customer relationship management and provide visibility into sales opportunities and customer activities.

## 5.13.2 CRM Requirements

- Customer lead registration.
- Opportunity management.
- Sales activity tracking.
- Customer communication history.
- Quotation follow-up.
- Customer segmentation.
- Sales pipeline reporting.
- Conversion rate monitoring.

## 5.13.3 Customer Segmentation

| Segment | Description |
|---|---|
| Platinum | Strategic high-volume accounts |
| Gold | Established high-value customers |
| Silver | Medium-volume customers |
| Standard | Small retail customers |

### Portfolio Segmentation Rules

The following thresholds are dummy assumptions based on annual net sales:

| Segment | Annual Net Sales |
|---|---:|
| Platinum | At least IDR 2,000,000,000 |
| Gold | IDR 1,000,000,000–1,999,999,999 |
| Silver | IDR 250,000,000–999,999,999 |
| Standard | Below IDR 250,000,000 |

Customer segmentation is reviewed quarterly. Management may approve a manual strategic classification, but the reason and approver must be recorded.

---

# 5.14 APPROVAL AND INTERNAL CONTROL

## 5.14.1 Business Objective

Establish accountability and prevent unauthorized business transactions.

## 5.14.2 Approval Requirements

Controlled approvals are required for:

- Purchase orders.
- Sales discounts.
- Customer credit exceptions.
- Inventory adjustments.
- Stock write-offs.
- Supplier returns.
- Customer refunds.
- Exceptional pricing.
- Credit limit amendments.

## 5.14.3 Segregation of Duties

| Process | Responsible Role | Approval Role |
|---|---|---|
| Purchase Requisition | Procurement Staff | Procurement Supervisor |
| Purchase Order | Procurement Officer | Applicable Purchase Approver |
| Inventory Adjustment | Warehouse Staff | Applicable Inventory Approver |
| Credit Exception | Sales Staff | Finance Manager / Managing Director |
| Customer Refund | Customer Service | Finance Manager |
| Vendor Payment | Accounts Payable | Finance Manager |

A user must not approve their own transaction where the relevant segregation-of-duties policy prohibits it.

## 5.14.4 Approval Policy Summary

| Transaction | Approval Basis | Approval Policy |
|---|---|---|
| Purchase Order | PO value before tax | Purchase Approval Matrix |
| Sales Discount | Discount percentage per line | Sales Discount Matrix |
| Credit Exception | Exposure and overdue status | Credit Management Policy |
| Inventory Adjustment | Absolute inventory difference value | Inventory Adjustment Matrix |
| Customer Refund | Refund amount | Refund Approval Matrix |
| Supplier Return | Estimated return value | Purchase Approval Matrix or delegated authority |

### Customer Refund Approval Matrix

| Refund Value | Required Approval |
|---|---|
| Up to IDR 5,000,000 | Customer Service Supervisor and Finance review |
| Above IDR 5,000,000–25,000,000 | Finance Manager |
| Above IDR 25,000,000–100,000,000 | Finance Manager and Operations Manager |
| Above IDR 100,000,000 | Managing Director and Finance Manager |

## 5.14.5 Audit Trail

The system must maintain:

- Document creation history.
- Document modification history.
- Approval history.
- Transaction status changes.
- Inventory movement history.
- User activity references.
- Relevant financial transaction references.
- Credit exception history.
- Quality disposition history.

---

# 5.15 MANAGEMENT REPORTING AND BUSINESS INTELLIGENCE

## 5.15.1 Business Objective

Provide management with reliable operational and financial insights based on consistent transactional data.

## 5.15.2 Dashboard Definitions and KPI Formulas

### A. Inventory Dashboard

| KPI | Formula / Definition | Primary Data Source |
|---|---|---|
| Total Inventory Quantity | Sum of on-hand quantity for selected internal locations | Inventory quants |
| Total Inventory Valuation | Sum of inventory valuation for selected scope | Stock valuation records |
| Available Stock | On-hand quantity minus reserved quantity | Inventory quants and reservations |
| Below-Minimum Stock | Count of product-warehouse combinations with forecasted stock below minimum | Reordering rules and forecasted quantity |
| Overstocked Products | Count of product-warehouse combinations with forecasted stock above maximum | Reordering rules and forecasted quantity |
| Near-Expiration Quantity | Quantity in lots expiring within 90 days | Lot/expiration and stock records |
| Expired Quantity | Quantity in lots with expiration date earlier than report date | Lot/expiration and stock records |
| Inventory Aging | Quantity and value grouped by time since receipt | Stock movement and valuation history |
| Warehouse Stock Comparison | On-hand quantity or valuation grouped by warehouse | Inventory records |

**Inventory scope rules:**

- Internal warehouse locations are included.
- Supplier, customer, transit, and virtual adjustment locations are excluded from on-hand internal stock unless a report explicitly requests them.
- Quarantined and damaged inventory must be displayed separately from available stock.
- Inventory valuation must use accounting valuation records rather than sales prices.

### B. Sales Dashboard

| KPI | Formula / Definition | Primary Data Source |
|---|---|---|
| Net Sales Revenue | Posted sales invoice untaxed amount minus posted sales credit notes untaxed amount | Customer invoices and credit notes |
| Sales by Customer | Net sales grouped by customer | Customer invoices |
| Sales by Product | Net sales grouped by invoice product line | Invoice lines |
| Sales by Territory | Net sales grouped by assigned customer territory | Customer master and invoice lines |
| Sales by Salesperson | Net sales grouped by responsible salesperson | Sales orders and invoice lines |
| Sales Order Fulfillment | Delivered quantity ÷ ordered quantity × 100 | Sales order lines and delivery records |
| Outstanding Receivables | Posted receivable balances not fully reconciled | Accounting receivable lines |
| Sales Return Analysis | Return quantity and value grouped by return reason | Return records and credit notes |

**Sales revenue rules:**

- Draft and cancelled invoices are excluded.
- Posted credit notes reduce net sales.
- Taxes are excluded from net sales revenue.
- The dashboard period is based on invoice date unless a report explicitly uses order date or delivery date.

### C. Procurement Dashboard

| KPI | Formula / Definition | Primary Data Source |
|---|---|---|
| Total Purchasing Value | Confirmed PO untaxed value for selected period | Purchase orders |
| PO by Vendor | PO count and value grouped by vendor | Purchase orders |
| PO by Status | Count of PO grouped by current status | Purchase orders |
| Vendor Delivery Performance | Vendor KPI formulas defined in Section 5.12 | PO and receipt records |
| Purchase Price Trend | Weighted average purchase unit price by product and period | Purchase order lines |
| Outstanding PO Value | Confirmed PO value not yet fully received or cancelled | Purchase orders and receipts |
| Procurement Lead Time | Average days between PO confirmation and validated receipt | Purchase and stock records |

### D. Warehouse Dashboard

| KPI | Formula / Definition | Primary Data Source |
|---|---|---|
| Incoming Goods Volume | Quantity received during selected period | Validated receipts |
| Outgoing Goods Volume | Quantity dispatched during selected period | Validated deliveries |
| Picking Productivity | Total picked lines or units divided by recorded picking hours | Picking records and time records where available |
| Packing Productivity | Total packed packages divided by recorded packing hours | Packing records and time records where available |
| Inventory Discrepancies | Count and value of approved inventory adjustments | Inventory adjustment records |
| Stock Transfer Performance | Completed transfer quantity ÷ requested transfer quantity × 100 | Internal transfer records |
| Return Processing Volume | Number and quantity of processed return records | Return records |

Where time data is not captured, productivity must be shown as transaction volume only and must not be presented as units per hour.

### E. Financial Dashboard

| KPI | Formula / Definition | Primary Data Source |
|---|---|---|
| Accounts Receivable | Outstanding posted receivable balances | General ledger |
| Accounts Payable | Outstanding posted payable balances | General ledger |
| Overdue Receivables | Receivable balances past due date | Receivable aging |
| Cash and Bank Balances | Posted cash and bank account balances | General ledger |
| Gross Profit | Net sales revenue minus recognized COGS | Accounting entries |
| Inventory Valuation | Posted inventory valuation | Stock valuation records |
| Profit and Loss | Standard financial statement calculation | General ledger |

## 5.15.3 Dashboard Refresh and Data Governance

| Report Type | Expected Refresh |
|---|---|
| Operational stock indicators | Near real-time after validated stock transactions |
| Sales and procurement transaction reports | On-demand from transactional records |
| Vendor scorecard | Monthly calculation |
| Financial statements | Based on posted accounting entries |
| Management KPI summary | Daily refresh for the portfolio dashboard |

All dashboard figures must be traceable to their source records.

A dashboard must not display a KPI as actual performance when the underlying source data is incomplete or unavailable. In that situation, the report must show an appropriate status such as **Insufficient Data**, **Not Available**, or **Pending Reconciliation**.

## 5.15.4 Reporting Requirements

- Date filtering.
- Warehouse filtering.
- Product category filtering.
- Customer and vendor filtering.
- Export capabilities where appropriate.
- Financial reports based on validated accounting data.
- Dashboard metrics traceable to underlying records.
- Consistent KPI definitions across reports.
- Access restrictions according to user roles.

---

# 6. END-TO-END BUSINESS SCENARIOS

The following scenarios are mandatory portfolio demonstration scenarios.

| Scenario ID | Scenario | Primary Business Domains |
|---|---|---|
| E2E-001 | Procure to Pay | Procurement, Inventory, Quality, Accounting |
| E2E-002 | Order to Cash | Sales, Inventory, Warehouse, Accounting |
| E2E-003 | Multi-Warehouse Replenishment | Inventory, Warehouse, Supply Chain |
| E2E-004 | Lot and Expiration Management | Inventory, Warehouse, Quality |
| E2E-005 | Customer Credit Limit Violation | Sales, Credit Management, Finance |
| E2E-006 | Supplier Delivery Discrepancy | Procurement, Warehouse, Quality |
| E2E-007 | Customer Return and Refund | Sales, Returns, Warehouse, Finance |
| E2E-008 | Imported Goods and Landed Costs | Procurement, Inventory, Accounting |
| E2E-009 | Inventory Adjustment and Cycle Counting | Inventory, Warehouse, Accounting |
| E2E-010 | Vendor Performance Evaluation | Procurement, Quality, Reporting |

## 6.1 Scenario 01 – Procure to Pay (P2P)

**Objective:** Demonstrate the complete purchasing lifecycle.

Business flow:

1. Identify inventory shortage.
2. Generate replenishment requirement.
3. Prepare purchase requisition.
4. Request supplier quotations.
5. Compare supplier offers.
6. Select preferred supplier.
7. Submit purchase order for approval.
8. Confirm purchase order.
9. Receive incoming goods.
10. Perform quantity and quality checks.
11. Validate goods receipt.
12. Receive supplier invoice.
13. Perform three-way matching.
14. Approve vendor bill.
15. Register supplier payment.
16. Reconcile payment.

**Expected outcome:** Complete procurement traceability from replenishment requirement to financial settlement.

## 6.2 Scenario 02 – Order to Cash (O2C)

**Objective:** Demonstrate the complete customer sales lifecycle.

Business flow:

1. Register customer inquiry.
2. Prepare quotation.
3. Apply customer-specific pricing.
4. Validate customer credit.
5. Confirm sales order.
6. Reserve available stock.
7. Generate warehouse delivery.
8. Pick and pack products.
9. Validate delivery.
10. Generate customer invoice.
11. Register customer payment.
12. Reconcile receivables.

**Expected outcome:** Complete sales traceability from quotation to customer payment.

## 6.3 Scenario 03 – Multi-Warehouse Replenishment

**Objective:** Demonstrate stock redistribution between regional warehouses.

Business flow:

1. Bandung stock reaches minimum level.
2. Replenishment requirement is identified.
3. Jakarta stock availability is checked.
4. Internal transfer is requested.
5. Transfer is approved.
6. Goods are picked and dispatched.
7. Goods are received in Bandung.
8. Destination inventory is updated.

**Expected outcome:** Accurate stock visibility and traceable warehouse transfers.

## 6.4 Scenario 04 – Lot and Expiration Management

**Objective:** Demonstrate product traceability and expiration control.

Business flow:

1. Receive products with lot numbers.
2. Record expiration dates.
3. Store products in designated locations.
4. Allocate stock using FEFO.
5. Deliver products to customers.
6. Trace delivered products using lot information.
7. Identify remaining stock from a specific lot.
8. Simulate product recall.

**Expected outcome:** Full traceability from supplier receipt to customer delivery.

## 6.5 Scenario 05 – Customer Credit Limit Violation

**Objective:** Demonstrate financial risk control.

Business flow:

1. Customer requests a new order.
2. Sales representative creates quotation.
3. System evaluates customer exposure.
4. Credit limit is exceeded.
5. Sales order requires authorized review.
6. Finance Manager evaluates the request.
7. Approval or rejection is recorded.

**Expected outcome:** Unauthorized credit exposure is prevented.

## 6.6 Scenario 06 – Supplier Delivery Discrepancy

**Objective:** Demonstrate procurement and warehouse exception handling.

Business flow:

1. Purchase order is confirmed for 1,000 units.
2. Supplier delivers 950 units.
3. Warehouse records actual quantity.
4. Outstanding quantity is identified.
5. Procurement contacts supplier.
6. Supplier confirms remaining delivery.
7. Remaining 50 units are received later.
8. Purchase order is completed.

**Expected outcome:** Partial receipt and outstanding purchase quantity are properly managed.

## 6.7 Scenario 07 – Customer Return and Refund

**Objective:** Demonstrate reverse logistics and financial integration.

Business flow:

1. Customer reports damaged products.
2. Customer Service creates return request.
3. Return is authorized.
4. Warehouse receives returned goods.
5. Quality inspection is performed.
6. Goods are transferred to damaged stock.
7. Finance processes credit note or refund.
8. Customer receivable is adjusted.

**Expected outcome:** Return transactions remain traceable and financially accurate.

## 6.8 Scenario 08 – Imported Goods and Landed Costs

**Objective:** Demonstrate international procurement and acquisition cost allocation.

Business flow:

1. Create international purchase order.
2. Confirm vendor order.
3. Receive imported products.
4. Record import-related costs.
5. Prepare landed cost document.
6. Allocate additional acquisition costs.
7. Validate landed cost.
8. Review updated inventory valuation.

**Expected outcome:** Imported product costs reflect eligible acquisition expenses according to the approved allocation policy.

## 6.9 Scenario 09 – Inventory Adjustment and Cycle Counting

**Objective:** Demonstrate inventory control and discrepancy management.

Business flow:

1. Schedule cycle count.
2. Generate inventory counting assignment.
3. Perform physical stock count.
4. Compare physical and recorded quantities.
5. Identify discrepancy.
6. Submit adjustment for approval.
7. Validate approved adjustment.
8. Review resulting inventory valuation.

**Expected outcome:** Inventory discrepancies are controlled and auditable.

## 6.10 Scenario 10 – Vendor Performance Evaluation

**Objective:** Demonstrate supplier performance monitoring.

Business flow:

1. Collect historical purchase transactions.
2. Analyze supplier delivery performance.
3. Evaluate order fulfillment.
4. Review quality inspection results.
5. Calculate performance indicators.
6. Generate supplier performance report.
7. Support future procurement decisions.

**Expected outcome:** Supplier evaluation is based on operational evidence and defined KPI formulas.

---

# 7. DATA MIGRATION AND DUMMY DATA REQUIREMENTS

## 7.1 Business Objective

Prepare structured and consistent dummy data to support initial ERP configuration, master data migration, opening balances, transaction testing, and portfolio demonstration.

All records must be fictional and must not contain real personal or company confidential information.

## 7.2 Target Data Volume

| Data Category | Target Volume | Purpose |
|---|---:|---|
| Products | 500 | Product master |
| Customers | 250 | Customer master |
| Vendors | 40 | Supplier master |
| Warehouses | 3 | Warehouse configuration |
| Internal Locations | 30+ | Storage structure |
| ERP Users | 20 | Role and access testing |
| Historical Sales Orders | 1,000 | Sales history and reporting |
| Historical Purchase Orders | 300 | Procurement history |
| Opening Lots | 100 | Traceability testing |
| Opening Stock Records | 500+ | Initial inventory |
| Opening Customer Balances | 250 or fewer | Receivable opening data |
| Opening Vendor Balances | 40 or fewer | Payable opening data |

The target volume is a portfolio dataset specification, not an assertion that these records have already been created or migrated.

## 7.3 Data Migration Scope

| Data Set | Required Fields |
|---|---|
| Product Master | Internal reference, name, category, UoM, barcode, tracking, cost method category, sales price, purchase price |
| Customer Master | Customer code, name, type, address, payment terms, credit limit, tax identification placeholder, salesperson |
| Vendor Master | Vendor code, name, country, payment terms, lead time, product references |
| Warehouse | Warehouse code, name, location |
| Internal Locations | Location code, parent location, location type, warehouse |
| Opening Inventory | Product, warehouse, location, quantity, UoM, lot/serial, expiration date, unit cost |
| Customer Opening Balance | Customer, invoice reference, invoice date, due date, residual amount |
| Vendor Opening Balance | Vendor, bill reference, bill date, due date, residual amount |
| Historical Sales | Order reference, customer, product, quantity, price, date, status |
| Historical Purchases | PO reference, vendor, product, quantity, unit price, order date, receipt date, status |

## 7.4 Data Preparation Rules

1. Each master record must have a unique identifier.
2. Product references must be unique.
3. Customer and vendor codes must be unique.
4. UoM values must use standardized naming.
5. Product categories must exist before product import.
6. Warehouse and location structures must exist before opening stock import.
7. Tracked products must have valid lot or serial information.
8. Products with expiration tracking must have valid expiration dates.
9. Opening stock quantities must be reconciled against the opening inventory file.
10. Customer and vendor opening balances must be reconciled against the dummy opening trial balance.
11. Historical transactions must not be imported as if they were current open transactions unless explicitly required.
12. Imported records must preserve references between related business documents.

## 7.5 Import Validation

| Validation ID | Validation Rule | Acceptance Criteria |
|---|---|---|
| MIG-001 | Unique master references | No duplicate internal references |
| MIG-002 | Product category mapping | 100% of products mapped to valid categories |
| MIG-003 | UoM mapping | 100% of products mapped to valid UoMs |
| MIG-004 | Customer and vendor references | No duplicate partner codes |
| MIG-005 | Warehouse mapping | All stock records reference valid warehouses |
| MIG-006 | Location mapping | All stock records reference valid internal locations |
| MIG-007 | Lot and serial tracking | All tracked opening stock has valid identification |
| MIG-008 | Expiration dates | All designated perishable lots have valid dates |
| MIG-009 | Opening quantity | Imported quantity matches approved dummy opening file |
| MIG-010 | Opening valuation | Imported inventory value reconciles to approved opening value |
| MIG-011 | Opening receivables/payables | Balances reconcile to dummy opening accounting data |
| MIG-012 | Import error handling | Rejected rows are logged and can be corrected |

## 7.6 Data Migration Deliverables

- Product master import template.
- Customer master import template.
- Vendor master import template.
- Warehouse and location import template.
- Opening stock import template.
- Lot and serial import template.
- Customer opening balance template.
- Vendor opening balance template.
- Historical transaction sample dataset.
- Data cleansing and validation log.
- Import execution evidence.
- Reconciliation report.

## 7.7 Data Ownership

| Data Set | Data Owner | Reviewer |
|---|---|---|
| Product Master | Inventory Controller | Operations Manager |
| Customer Master | Sales Administration | Sales Manager |
| Vendor Master | Procurement Officer | Procurement Manager |
| Warehouse and Locations | Warehouse Supervisor | Operations Manager |
| Opening Stock | Inventory Controller | Finance Manager |
| Opening Receivables | Accounts Receivable | Finance Manager |
| Opening Payables | Accounts Payable | Finance Manager |
| Accounting Opening Balances | Finance Department | Finance Manager |

---

# 8. NON-FUNCTIONAL REQUIREMENTS

## 8.1 Performance

- Normal business transactions should respond within an acceptable operational timeframe.
- Standard form operations should target approximately 3 seconds under the agreed test environment.
- Management reports should execute within acceptable business reporting windows.
- Database queries should be optimized for expected transaction volumes.
- Batch operations must avoid unnecessary performance degradation.
- Performance targets must be validated using realistic test data and documented test conditions.

## 8.2 Security

- User authentication is mandatory.
- Access must be role-based.
- Sensitive financial information must be restricted.
- Warehouse users must access only authorized operational areas.
- Approval permissions must be separated from normal transaction permissions.
- Unauthorized record modification must be prevented.
- User activities must be traceable.

## 8.3 Availability

- The system must support normal business operating hours.
- Database backup procedures must be established.
- Recovery procedures must be documented.
- System failures must be logged.
- Deployment must support service restart and recovery.

## 8.4 Data Integrity

- Master data must maintain unique references.
- Transactions must maintain valid relationships.
- Inventory movements must remain traceable.
- Financial transactions must preserve accounting integrity.
- Deleted or cancelled business documents must not silently corrupt historical records.

## 8.5 Scalability

The architecture must accommodate:

- Additional warehouses.
- More customers and suppliers.
- Larger product catalogs.
- Increased transaction volumes.
- Additional business users.
- Future custom modules.

## 8.6 Usability

- Interfaces must be understandable to operational users.
- Standardized naming conventions must be applied.
- Forms must provide meaningful validation.
- Reports must use clear business terminology.
- Users must receive appropriate training.

---

# 9. USER ROLES AND RESPONSIBILITIES

The ERP system must support role-based access control.

| Role | Main Responsibilities |
|---|---|
| System Administrator | Technical system configuration |
| ERP Manager | Functional administration |
| Sales Representative | Customer quotations and sales |
| Sales Supervisor | Sales supervision |
| Sales Manager | Sales approvals |
| Procurement Officer | Supplier sourcing and purchasing |
| Procurement Supervisor | Procurement review |
| Procurement Manager | Procurement approval |
| Warehouse Operator | Receiving, picking, packing |
| Warehouse Supervisor | Warehouse supervision |
| Warehouse Manager | Warehouse approval |
| Inventory Controller | Stock reconciliation and reporting |
| Quality Inspector | Product inspections |
| Logistics Coordinator | Shipment coordination |
| Customer Service | Customer complaints and returns |
| Accounts Receivable | Customer invoicing and collection |
| Accounts Payable | Supplier invoices and payments |
| Finance Manager | Financial control and approval |
| Operations Manager | Operational oversight |
| Managing Director | Executive oversight |

Access permissions must follow the principle of least privilege.

---

# 10. PROJECT ASSUMPTIONS

The project is based on the following assumptions:

| ID | Assumption |
|---|---|
| ASM-001 | The company operates as a single legal entity |
| ASM-002 | The company uses IDR as its primary currency |
| ASM-003 | The company operates three distribution warehouses |
| ASM-004 | The company follows a B2B distribution model |
| ASM-005 | The initial product catalog contains 500 SKUs |
| ASM-006 | The company has 250 active customers |
| ASM-007 | The company has 40 active suppliers |
| ASM-008 | Selected products require lot tracking |
| ASM-009 | Selected products require serial tracking |
| ASM-010 | Perishable products require expiration tracking |
| ASM-011 | The company uses the dummy costing matrix defined in this BRD |
| ASM-012 | The company uses the dummy approval policies defined in this BRD |
| ASM-013 | The company uses the illustrative tax assumptions defined in this BRD |
| ASM-014 | All sample records are fictional |
| ASM-015 | Historical transactions are created for portfolio testing |
| ASM-016 | Accounting opening balances are prepared and reconciled before migration |
| ASM-017 | Users and roles are assigned according to the defined organizational structure |
| ASM-018 | Odoo 19 Enterprise is the target ERP platform |

---

# 11. PROJECT DEPENDENCIES

| ID | Dependency | Responsible Party |
|---|---|---|
| DEP-001 | BRD review and baseline approval | Project Sponsor / Stakeholders |
| DEP-002 | Approved business policies | Relevant Business Managers |
| DEP-003 | Product, customer, and vendor master data | Business Departments |
| DEP-004 | Opening inventory data | Inventory Controller |
| DEP-005 | Accounting opening balances | Finance Manager |
| DEP-006 | Indonesian tax configuration validation | Finance Manager / Tax Advisor |
| DEP-007 | Odoo Enterprise environment | ERP Technical Team |
| DEP-008 | User role and access definition | ERP Manager |
| DEP-009 | Warehouse and inventory SOP | Operations Manager |
| DEP-010 | Test scenarios and expected results | Business Owners |
| DEP-011 | Dummy dataset preparation | ERP Implementation Team |
| DEP-012 | Infrastructure and backup readiness | IT Department |

---

# 12. PROJECT RISKS AND MITIGATION

| Risk ID | Risk | Impact | Mitigation |
|---|---|---|---|
| RSK-001 | Inconsistent master data | Incorrect transactions | Data cleansing and validation |
| RSK-002 | Incorrect opening stock | Inventory discrepancies | Physical count simulation and reconciliation |
| RSK-003 | Incorrect accounting configuration | Financial misstatement | Finance review and controlled testing |
| RSK-004 | User resistance | Low adoption | Training and SOP documentation |
| RSK-005 | Incorrect access permissions | Unauthorized transactions | Role-based access review |
| RSK-006 | Unclear warehouse SOP | Operational inconsistency | Standardized process documentation |
| RSK-007 | Custom module defects | Transaction errors | Automated and manual testing |
| RSK-008 | Integration issues | Inconsistent data | Integration testing |
| RSK-009 | Poor performance | Operational delays | Performance testing |
| RSK-010 | Backup failure | Data loss | Backup and recovery testing |
| RSK-011 | Incorrect lot and expiry data | Product traceability failure | Import validation |
| RSK-012 | Incorrect landed cost allocation | Incorrect inventory valuation | Finance reconciliation |
| RSK-013 | Incorrect credit exposure calculation | Excessive customer credit risk | Reconciliation against accounting balances and order commitments |
| RSK-014 | Incorrect KPI source data | Misleading management reports | KPI reconciliation and data lineage review |
| RSK-015 | Incorrect tax assumptions | Incorrect tax postings | Explicit portfolio labeling and Finance validation |

---

# 13. IMPLEMENTATION SUCCESS AND ACCEPTANCE CRITERIA

The project will be considered functionally successful when the defined business processes and system controls operate according to the approved requirements.

## 13.1 Functional Acceptance

- Master data can be created and maintained.
- Sales quotations can be converted into sales orders.
- Customer credit controls operate according to the approved dummy policy.
- Purchase requisitions and purchase orders can be processed.
- Purchase approvals follow the defined approval matrix.
- Goods receipts support partial deliveries.
- Inventory is updated correctly after stock movements.
- Lot and serial tracking work for designated products.
- Expiration dates are properly managed.
- FEFO allocation works for applicable products.
- Multi-warehouse transfers are traceable.
- Customer returns and supplier returns are supported.
- Inventory valuation is integrated with accounting.
- Vendor bills can be matched against purchasing and receiving records.
- Quality inspection checklists enforce defined acceptance criteria.
- Vendor performance calculations use documented formulas.
- Management reports provide consistent transactional information.
- Customer credit exposure is calculated without double-counting order and invoice obligations.
- Data migration templates and validation procedures are available.

## 13.2 Technical Acceptance

- Custom modules install without critical errors.
- Custom models and business logic behave as specified.
- Access controls prevent unauthorized transactions.
- Required automated jobs execute successfully.
- APIs handle valid and invalid requests appropriately.
- Automated tests pass.
- Database backup and recovery are demonstrated.
- Deployment documentation is available.
- KPI calculations can be reconciled to their source data.
- Import validation errors are logged and traceable.

## 13.3 Operational Acceptance

- Users can execute assigned business processes.
- Standard operating procedures are documented.
- Training materials are available.
- Critical business scenarios are successfully tested.
- No unresolved critical defects remain.
- UAT approval is documented.
- Business owners accept the implemented workflows.
- Opening data reconciliation is documented.

## 13.4 Portfolio KPI Targets

These targets are fictional project success criteria. They are not actual achieved results.

| KPI | Target | Measurement |
|---|---:|---|
| Inventory Accuracy | ≥98% | Correct counted quantity ÷ total counted quantity × 100 |
| On-Time Delivery | ≥95% | On-time deliveries ÷ eligible deliveries × 100 |
| Order Fulfillment | ≥97% | Delivered quantity ÷ ordered quantity × 100 |
| Supplier On-Time Delivery | ≥95% | On-time receipts ÷ eligible receipts × 100 |
| Quality Acceptance | ≥99% | Accepted inspected quantity ÷ total inspected quantity × 100 |
| Product Traceability | 100% | Tracked movements with valid lot/serial references ÷ tracked movements × 100 |
| Expired Product Sales | 0 | Number of validated sales deliveries containing expired products |
| Data Migration Accuracy | ≥99.5% | Validated imported records ÷ total imported records × 100 |
| Critical Defects at UAT Sign-Off | 0 | Open critical defects |
| Credit Control Compliance | 100% | Credit-controlled transactions following approval policy ÷ applicable transactions × 100 |

---

# 14. REQUIREMENTS PRIORITIZATION

Requirements will be prioritized using the MoSCoW method.

| Priority | Definition |
|---|---|
| Must Have | Mandatory for core business operation |
| Should Have | Important, but temporary workaround may exist |
| Could Have | Useful enhancement that can be deferred |
| Won't Have | Explicitly excluded from current implementation |

Requirements marked Must Have form the baseline for initial functional acceptance.

Any priority change after baseline approval must be recorded through change control.

---

# 15. OPEN POLICY AND DECISION REGISTER

The following register distinguishes the policies defined by this revised BRD from items that still require detailed design or validation.

| Decision ID | Area | Portfolio Decision in BRD | Remaining Validation |
|---|---|---|---|
| DEC-001 | Purchase Approval | Thresholds defined in Section 5.3.5 | Validate approval routing in Odoo |
| DEC-002 | Sales Discounts | Discount tiers defined in Section 5.2.6 | Validate approval behavior |
| DEC-003 | Inventory Adjustments | Value-based approval tiers defined in Section 5.4.5 | Validate valuation calculation and approval flow |
| DEC-004 | Costing | FIFO/AVCO defined per product category | Validate accounting configuration and valuation behavior |
| DEC-005 | Indonesian Tax | Illustrative 11% dummy tax assumptions | Must be validated before any real deployment |
| DEC-006 | Credit Management | Exposure formula and hold rules defined | Validate data sources and avoid double-counting |
| DEC-007 | Quality | Measurable inspection criteria defined | Confirm checklist implementation and disposition |
| DEC-008 | Vendor Performance | KPI formulas and weights defined | Validate source fields and sample-size rules |
| DEC-009 | Reporting | KPI formulas and sources defined | Validate dashboard reconciliation |
| DEC-010 | Data Migration | Data volumes and templates defined | Generate, cleanse, and validate actual dummy datasets |
| DEC-011 | Refund Approval | Value-based approval matrix defined | Validate workflow and segregation of duties |
| DEC-012 | Landed Cost | Allocation method assigned by cost type | Validate accounting treatment and allocation behavior |

A policy being defined in this BRD does not mean it has already been configured or tested in Odoo.

---

# 16. GLOSSARY

| Term | Definition |
|---|---|
| ERP | Enterprise Resource Planning |
| BRD | Business Requirements Document |
| SOW | Scope of Work |
| FSD | Functional Specification Document |
| TDD | Technical Design Document |
| SKU | Stock Keeping Unit |
| UoM | Unit of Measure |
| RFQ | Request for Quotation |
| PO | Purchase Order |
| SO | Sales Order |
| P2P | Procure to Pay |
| O2C | Order to Cash |
| FEFO | First Expired, First Out |
| FIFO | First In, First Out |
| AVCO | Average Cost |
| MOQ | Minimum Order Quantity |
| SLA | Service Level Agreement |
| KPI | Key Performance Indicator |
| UAT | User Acceptance Testing |
| RTM | Requirements Traceability Matrix |
| COGS | Cost of Goods Sold |
| WMS | Warehouse Management System |
| GRN | Goods Received Note |
| POD | Proof of Delivery |
| PPN | Pajak Pertambahan Nilai |
| ACL | Access Control List |
| ORM | Object Relational Mapping |
| OTD | On-Time Delivery |
| AR | Accounts Receivable |
| AP | Accounts Payable |
| DPP | Dasar Pengenaan Pajak |

---

# 17. BRD CONCLUSION

The Advanced Wholesale Distribution & Supply Chain ERP implementation aims to transform PT Arunika Distribusi Nusantara from fragmented operational management into an integrated, centralized, and controlled enterprise distribution environment.

The revised BRD defines the company's fictional business policies and requirements across procurement, warehouse operations, inventory management, sales, logistics, quality management, accounting, credit management, supplier management, and reporting.

Version 1.1 provides more specific business rules for previously ambiguous areas, including:

- Purchase and sales approval thresholds.
- Inventory adjustment approval.
- Product-category costing methods.
- Illustrative Indonesian tax configuration.
- Customer credit exposure and blocking rules.
- Measurable quality inspection criteria.
- Vendor performance formulas and source data.
- Dashboard KPI formulas and data lineage.
- Data migration scope, volume, and validation criteria.

Odoo 19 Enterprise will serve as the central ERP platform, supported by appropriate standard configuration, automation, custom module development, and integration where justified by fit-gap analysis.

This document will serve as the business requirements reference for the subsequent SOW, process mapping, FSD, Fit-Gap Analysis, TDD, implementation, and testing deliverables.

**The document remains a Revised Draft until the portfolio approval process is completed.**

---

# 18. NEXT DOCUMENTS AND PROJECT DELIVERABLES

| Sequence | Document | Purpose |
|---|---|---|
| 01 | Business Requirements Document (BRD) | Defines business needs and processes |
| 02 | Scope of Work (SOW) | Defines implementation boundaries and deliverables |
| 03 | Business Process Mapping | Defines AS-IS and TO-BE business processes |
| 04 | Functional Specification Document (FSD) | Defines functional behavior and workflows |
| 05 | Fit-Gap Analysis | Determines standard configuration, customization, integration, or exclusions |
| 06 | Technical Design Document (TDD) | Defines architecture and technical implementation |
| 07 | Configuration & Development Guide | Documents actual Odoo implementation |
| 08 | Test Strategy & Test Cases | Defines testing coverage |
| 09 | Test Execution Evidence | Documents test results |
| 10 | Requirements Traceability Matrix | Connects requirements to implementation and tests |
| 11 | UAT & Defect Summary | Records user acceptance and defects |
| 12 | Deployment & Handover Guide | Documents production-like deployment |

## DOCUMENT END

**Document ID:** ADN-BRD-001  
**Project:** Advanced Wholesale Distribution & Supply Chain ERP  
**Organization:** PT Arunika Distribusi Nusantara  
**ERP Platform:** Odoo 19 Enterprise  
**Version:** 1.1  
**Status:** Approved
**Classification:** Portfolio / Fictional Business Case