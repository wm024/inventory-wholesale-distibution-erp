# BUSINESS REQUIREMENTS DOCUMENT (BRD)

## Advanced Wholesale Distribution & Supply Chain ERP

**Project Name:** Advanced Wholesale Distribution & Supply Chain ERP Implementation  
**Company:** PT Arunika Distribusi Nusantara  
**ERP Platform:** Odoo 19 Enterprise  
**Deployment Model:** On-Premise  
**Operating System:** Ubuntu Linux  
**Database:** PostgreSQL  
**Document Type:** Business Requirements Document (BRD)  
**Document Version:** 1.0  
**Document Status:** Baseline – Draft for Portfolio Implementation  
**Prepared For:** ERP Implementation Case Study  
**Prepared By:** ERP Implementation Consultant  
**Date:** 12 November 2026

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
| Version | 1.0 |
| Status | Draft for Baseline |
| Classification | Portfolio / Fictional Business Case |

## 2. Revision History

| Version | Date | Description | Author |
|---|---|---|---|
| 1.0 | 12-Nov-2026 | Initial BRD preparation | ERP Business Analyst |

## 3. Approval Matrix

| Role | Responsibility | Approval Status |
|---|---|---|
| Project Sponsor | Business direction and budget approval | Pending |
| Managing Director | Executive approval | Pending |
| Operations Manager | Warehouse and distribution requirements | Pending |
| Procurement Manager | Purchasing requirements | Pending |
| Sales Manager | Sales and customer requirements | Pending |
| Finance Manager | Accounting and financial requirements | Pending |
| ERP Project Manager | Project coordination | Pending |

*All company names, personnel, transactions, financial figures, addresses, and business scenarios in this document are fictional and created exclusively for portfolio demonstration.*

---

# 1. EXECUTIVE SUMMARY

## 1.1 Business Overview

PT Arunika Distribusi Nusantara is a fictional Indonesian wholesale distribution company specializing in the procurement, storage, and distribution of Fast-Moving Consumer Goods (FMCG), household products, and consumer goods.

The company operates a Business-to-Business (B2B) distribution model, supplying products to:

- Traditional retail stores.
- Minimarkets and independent supermarkets.
- Wholesale merchants.
- Regional distributors.
- Corporate customers.
- Food service and hospitality businesses.

The company purchases products from local manufacturers, national suppliers, and international vendors before distributing them to customers through a network of regional warehouses.

As the company expands, its operational complexity increases, particularly in inventory management, procurement planning, order fulfillment, financial control, and inter-warehouse coordination.

The current business environment relies on fragmented operational tools, spreadsheets, and partially integrated applications. This creates operational inefficiencies and limits management's ability to obtain accurate, real-time business information.

The company therefore plans to implement an integrated Enterprise Resource Planning (ERP) system using Odoo 19 Enterprise.

The implementation aims to establish a centralized operational platform that connects:

1. Sales Management.
2. Purchase Management.
3. Inventory and Warehouse Management.
4. Supply Chain and Replenishment.
5. Accounting and Financial Management.
6. Customer Relationship Management.
7. Vendor Management.
8. Reporting and Business Intelligence.

The system must support end-to-end business processes, from procurement planning and supplier purchasing through warehouse receiving, inventory allocation, order fulfillment, delivery, invoicing, and payment reconciliation.

## 1.2 Project Vision

To establish a scalable, integrated, and data-driven distribution management system that improves operational efficiency, inventory accuracy, financial visibility, and customer service.

## 1.3 Project Objectives

The project has the following business objectives:

| ID | Objective | Expected Business Outcome |
|---|---|---|
| OBJ-001 | Centralize business operations | Unified ERP platform |
| OBJ-002 | Improve inventory accuracy | More reliable inventory records |
| OBJ-003 | Optimize procurement | Better purchasing decisions |
| OBJ-004 | Improve warehouse efficiency | Faster picking and fulfillment |
| OBJ-005 | Improve order management | Reduced order processing time |
| OBJ-006 | Strengthen financial control | Accurate receivables and payables |
| OBJ-007 | Improve supplier management | Measurable vendor performance |
| OBJ-008 | Improve management visibility | Centralized operational reporting |
| OBJ-009 | Support business scalability | Standardized multi-warehouse processes |
| OBJ-010 | Improve product traceability | End-to-end lot and expiration tracking |

## 1.4 Expected Business Benefits

The expected benefits include:

- Reduced manual data entry.
- Improved inventory visibility across all warehouses.
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
| Currency | Indonesian Rupiah (IDR) |
| Fiscal Year | January – December |
| Business Model | Business-to-Business Distribution |
| Number of Employees | 85 |
| Active Customers | 250 |
| Active Suppliers | 40 |
| Product Catalog | 500 SKUs |
| Distribution Warehouses | 3 |
| Sales Territories | 5 |

## 2.2 Business Locations

The company operates three distribution warehouses.

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

The company operates through the following departments:

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

The company operates through the following business cycle:

1. Demand identification.
2. Inventory availability assessment.
3. Procurement planning.
4. Supplier quotation and selection.
5. Purchase order creation.
6. Goods receiving.
7. Quality and quantity verification.
8. Inventory storage.
9. Customer order creation.
10. Stock reservation.
11. Picking and packing.
12. Delivery and shipment.
13. Customer invoicing.
14. Payment collection.
15. Financial reconciliation.
16. Management reporting.

The ERP system must provide integration and traceability across these processes.

---

# 3. CURRENT BUSINESS CHALLENGES

## 3.1 Existing Operational Environment

The company currently operates using a combination of:

- Microsoft Excel for inventory records.
- Spreadsheet-based purchasing plans.
- Manual sales order processing.
- Separate accounting applications.
- Manual warehouse stock reconciliation.
- Email and messaging applications for supplier communication.
- Manually prepared operational reports.

These applications operate independently and do not provide a centralized view of business operations.

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

The primary causes include:

1. Lack of centralized business data.
2. No standardized operational workflows.
3. Limited system-based internal controls.
4. Manual approval procedures.
5. Inconsistent master data.
6. Limited automation between departments.
7. Lack of real-time reporting.
8. Limited traceability between operational documents.

## 3.4 Business Transformation Requirements

The ERP implementation must address these challenges through standardized business processes, automated workflows, centralized information, and appropriate internal controls.

---

# 4. PROJECT SCOPE

## 4.1 In-Scope Business Areas

The project includes the following business domains:

| No. | Business Domain | Scope |
|---|---|---|
| 1 | Master Data Management | Products, customers, suppliers, and locations |
| 2 | Sales Management | Quotation, sales orders, delivery, and invoicing |
| 3 | Purchase Management | RFQ, vendor selection, and purchase orders |
| 4 | Inventory Management | Stock movement, adjustment, and traceability |
| 5 | Warehouse Management | Receiving, putaway, picking, and packing |
| 6 | Supply Chain | Replenishment and stock forecasting |
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
- Full transportation management system (TMS).
- Fleet maintenance management.
- Customer-facing mobile application development.
- Direct integration with every Indonesian marketplace.
- Advanced AI-based demand forecasting.
- Full customs brokerage integration.
- Automated bank statement connections.
- Advanced warehouse robotics integration.

These capabilities may be considered for future implementation phases.

## 4.3 Implementation Approach

The implementation will follow a phased approach:

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

The system must support centralized product registration and classification.

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

- Products must have unique internal references.
- Products must be assigned to appropriate categories.
- Products must support multiple units of measure where applicable.
- Products must support barcode identification.
- Products must support sales and purchase pricing.
- Products must support vendor-specific purchasing information.
- Selected products must support lot tracking.
- Selected products must support serial number tracking.
- Perishable products must have expiration date tracking.
- Products must support reorder rules.
- Product archival must not remove historical transaction records.

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

- Each customer must have a unique customer reference.
- Customer records must include contact information.
- Customers must have assigned payment terms.
- Customers must support individual credit limits.
- Customers must have assigned sales representatives.
- Customers must have designated delivery addresses.
- Customers must support tax identification information.
- Customers must be categorized according to customer type.
- Customer transactions must be traceable.

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

- Each supplier must have a unique vendor reference.
- Supplier products and purchase prices must be maintained.
- Supplier lead times must be recorded.
- Supplier payment terms must be defined.
- Supplier delivery performance must be measurable.
- Supplier quality performance must be recorded.
- Multiple vendors may supply the same product.
- Supplier records must maintain historical purchasing information.

## 5.1.5 Warehouse and Location Master

The system must support hierarchical warehouse locations.

### Sample Warehouse Structure

**WH-JKT – Jakarta Central Warehouse**

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

- Multiple warehouses must be supported.
- Each warehouse must have multiple internal locations.
- Warehouse locations must support barcode operations.
- Storage locations must support product-specific restrictions.
- Quarantine and damaged stock must be separated from available inventory.
- Inventory movements must maintain source and destination references.

---

# 5.2 SALES MANAGEMENT

## 5.2.1 Business Objective

Establish a standardized sales process from quotation creation through order fulfillment, invoicing, and payment collection.

## 5.2.2 Sales Business Model

The company operates a B2B sales model with the following order types:

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
| BR-SAL-001 | The system must support sales quotations. | Must |
| BR-SAL-002 | The system must convert confirmed quotations into sales orders. | Must |
| BR-SAL-003 | The system must support customer-specific pricing. | Must |
| BR-SAL-004 | The system must support volume-based discounts. | Must |
| BR-SAL-005 | The system must check product availability. | Must |
| BR-SAL-006 | The system must reserve inventory for confirmed orders. | Must |
| BR-SAL-007 | The system must support partial deliveries. | Must |
| BR-SAL-008 | The system must support backorders. | Must |
| BR-SAL-009 | The system must support sales returns. | Must |
| BR-SAL-010 | The system must support multiple delivery addresses. | Should |
| BR-SAL-011 | The system must support sales team assignments. | Must |
| BR-SAL-012 | The system must maintain sales order history. | Must |
| BR-SAL-013 | The system must support customer-specific payment terms. | Must |
| BR-SAL-014 | The system must support sales performance reporting. | Should |
| BR-SAL-015 | The system must support quotation expiration dates. | Should |

## 5.2.5 Customer Credit Management

The company requires credit control to prevent excessive outstanding receivables.

### Business Rules

- Each eligible customer must have an assigned credit limit.
- The system must monitor outstanding customer receivables.
- Sales orders exceeding the available credit limit must trigger a warning or approval requirement.
- Overdue receivables must be visible to the Finance Department.
- Credit limit exceptions must require authorized approval.
- Customers with overdue balances beyond company policy may be restricted from new credit sales.

### Example Scenario

Customer: PT Retail Makmur

| Description | Amount |
|---|---:|
| Credit Limit | IDR 100,000,000 |
| Existing Outstanding | IDR 75,000,000 |
| New Sales Order | IDR 40,000,000 |
| Projected Exposure | IDR 115,000,000 |
| Credit Excess | IDR 15,000,000 |

Expected result:

The system must identify the credit limit violation and prevent normal confirmation until the appropriate authorization is obtained.

## 5.2.6 Pricing and Discount Management

The company requires a structured pricing policy.

Example:

| Customer Category | Discount Policy |
|---|---|
| Retail Store | Standard pricing |
| Wholesaler | Volume-based discount |
| Supermarket | Contract pricing |
| Corporate Customer | Negotiated pricing |

Discount approval requirements:

- Discounts within the authorized sales representative threshold may be applied directly.
- Discounts exceeding the authorized threshold must require Sales Manager approval.
- Exceptional pricing must be recorded.
- Historical pricing must remain traceable.

---

# 5.3 PURCHASE MANAGEMENT

## 5.3.1 Business Objective

Establish a controlled procurement process that ensures products are purchased at competitive prices, in appropriate quantities, and within required delivery schedules.

## 5.3.2 Procurement Business Model

Procurement activities are triggered by:

- Reorder rules.
- Forecasted demand.
- Confirmed customer orders.
- Safety stock requirements.
- Seasonal demand.
- Management purchasing decisions.

The company purchases from both domestic and international suppliers.

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
| BR-PUR-001 | The system must support purchase requisitions. | Must |
| BR-PUR-002 | The system must support RFQ creation. | Must |
| BR-PUR-003 | The system must support multiple vendor quotations. | Must |
| BR-PUR-004 | The system must compare vendor prices. | Must |
| BR-PUR-005 | The system must maintain vendor lead times. | Must |
| BR-PUR-006 | The system must support purchase approval workflows. | Must |
| BR-PUR-007 | The system must support purchase order confirmation. | Must |
| BR-PUR-008 | The system must support partial supplier deliveries. | Must |
| BR-PUR-009 | The system must support purchase returns. | Must |
| BR-PUR-010 | The system must maintain purchase history. | Must |
| BR-PUR-011 | The system must support minimum order quantities. | Should |
| BR-PUR-012 | The system must support vendor performance evaluation. | Should |
| BR-PUR-013 | The system must support blanket purchase agreements. | Could |
| BR-PUR-014 | The system must support supplier price lists. | Must |

## 5.3.5 Purchase Approval Matrix

| Purchase Value | Required Approval |
|---|---|
| IDR 0 – 10,000,000 | Procurement Supervisor |
| IDR 10,000,001 – 50,000,000 | Procurement Manager |
| IDR 50,000,001 – 150,000,000 | Operations Manager |
| Above IDR 150,000,000 | Managing Director |

These thresholds are fictional business policy assumptions for the portfolio.

## 5.3.6 Procurement Example

The Jakarta warehouse requires additional mineral water inventory.

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

Expected result:

The system identifies the replenishment requirement, generates the purchasing proposal, and routes the purchase for approval.

---

# 5.4 INVENTORY MANAGEMENT

## 5.4.1 Business Objective

Provide accurate, real-time inventory visibility across all warehouses and establish strong controls over stock movement, traceability, and inventory valuation.

## 5.4.2 Inventory Management Requirements

| ID | Business Requirement | Priority |
|---|---|---|
| BR-INV-001 | The system must maintain real-time inventory balances. | Must |
| BR-INV-002 | The system must support multiple warehouses. | Must |
| BR-INV-003 | The system must support hierarchical storage locations. | Must |
| BR-INV-004 | The system must support lot tracking. | Must |
| BR-INV-005 | The system must support serial number tracking. | Must |
| BR-INV-006 | The system must support expiration date tracking. | Must |
| BR-INV-007 | The system must support FEFO allocation. | Must |
| BR-INV-008 | The system must support FIFO valuation where appropriate. | Must |
| BR-INV-009 | The system must support inventory adjustments. | Must |
| BR-INV-010 | The system must support cycle counting. | Must |
| BR-INV-011 | The system must support inventory reservations. | Must |
| BR-INV-012 | The system must support damaged inventory segregation. | Must |
| BR-INV-013 | The system must support inventory movement history. | Must |
| BR-INV-014 | The system must support stock aging reports. | Should |
| BR-INV-015 | The system must support inventory valuation reporting. | Must |

## 5.4.3 Lot and Expiration Management

The company handles products with different shelf-life requirements.

Example:

| Product | Lot Number | Manufacturing Date | Expiration Date | Quantity |
|---|---|---|---|---:|
| Mineral Water 600ml | LOT-MW-001 | 01-Nov-2026 | 01-Nov-2027 | 2,000 |
| Cooking Oil 1L | LOT-CO-001 | 15-Oct-2026 | 15-Oct-2027 | 1,500 |
| Detergent 800g | LOT-DT-001 | 20-Oct-2026 | 20-Oct-2028 | 1,000 |

Business rules:

- Tracked products must have valid lot or serial identification.
- Expiration dates must be recorded where applicable.
- Products approaching expiration must be identifiable.
- Expired goods must not be allocated for normal sales delivery.
- FEFO must be applied to eligible products.
- Lot information must remain traceable throughout inventory movements.
- Product recall must be supported through lot identification.

## 5.4.4 Inventory Valuation

The company requires accurate inventory valuation for financial reporting.

The following costing methods must be evaluated:

- FIFO.
- AVCO (Average Cost).

The final costing method must be assigned according to product category and approved accounting policy.

Business requirements:

- Inventory valuation must be reflected in financial records.
- Stock receipts and deliveries must create appropriate valuation entries.
- Inventory adjustments must be financially traceable.
- Inventory valuation reports must be available.
- Cost changes must be auditable.

## 5.4.5 Inventory Adjustment

The company requires a controlled process for stock discrepancies.

Example:

| Description | Quantity |
|---|---:|
| System Quantity | 1,000 |
| Physical Quantity | 970 |
| Difference | -30 |

Expected workflow:

1. Warehouse identifies the discrepancy.
2. Physical counting is recorded.
3. Inventory adjustment is prepared.
4. Supervisor reviews the discrepancy.
5. Authorized personnel approve the adjustment.
6. Inventory balance is updated.
7. Financial impact is recorded where applicable.

Material discrepancies must be escalated according to the approval matrix.

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

The system must support location assignment based on:

- Product category.
- Storage requirements.
- Warehouse capacity.
- Product compatibility.
- Storage zone.
- Handling requirements.

Example:

| Product Category | Preferred Location |
|---|---|
| Food & Beverage | Zone A |
| Household Cleaning | Zone B |
| Personal Care | Zone C |
| High-Value Goods | Secure Storage |
| Damaged Goods | Quarantine |

## 5.5.4 Order Picking

The warehouse must support structured picking operations.

Requirements:

- Picking operations must be generated from confirmed sales orders.
- Stock must be reserved according to availability.
- Lot selection must respect FEFO where applicable.
- Barcode scanning must be supported.
- Picking quantities must be verified.
- Short-picked quantities must be recorded.
- Partial deliveries must be supported.
- Picking operations must be traceable.

## 5.5.5 Packing and Dispatch

Requirements:

- Picked goods must be prepared for packing.
- Packing operations must be linked to delivery orders.
- Package identification must be supported.
- Dispatch confirmation must be recorded.
- Delivery documentation must be generated.
- Shipment tracking information must be recorded where available.

## 5.5.6 Warehouse Operational Scenarios

The implementation must demonstrate:

**Scenario A – Standard Receiving**

Supplier delivers 1,000 units against a confirmed purchase order.

**Scenario B – Partial Receiving**

Supplier delivers 700 units while 300 units remain outstanding.

**Scenario C – Quality Rejection**

Warehouse receives 500 units, of which 20 units are rejected.

**Scenario D – FEFO Picking**

Two lots of the same product have different expiration dates. The warehouse must prioritize the earliest-expiring eligible lot.

**Scenario E – Short Picking**

A customer orders 100 units, but only 80 units can be picked.

**Scenario F – Damaged Goods**

Warehouse discovers 15 damaged units during storage inspection and transfers them to a damaged inventory location.

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
| Replenishment Quantity | 4,200 Units |

The system must identify when forecasted stock falls below the minimum threshold and propose replenishment.

The proposed quantity must consider the maximum stock level and relevant purchasing constraints.

## 5.6.4 Inter-Warehouse Replenishment

The company must be able to transfer stock between warehouses.

Example:

Bandung warehouse has insufficient detergent stock, while Jakarta has surplus inventory.

| Description | Quantity |
|---|---:|
| Product | FreshClean Detergent 800g |
| Jakarta Available Stock | 5,000 |
| Bandung Available Stock | 300 |
| Bandung Minimum Stock | 1,000 |
| Proposed Transfer | 1,500 |

Expected process:

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

- Replenishment must be configurable by warehouse.
- The system must support minimum and maximum stock rules.
- The system must support safety stock.
- Replenishment must consider vendor lead times.
- Inter-warehouse transfers must be traceable.
- Transfers must support partial shipments.
- Transfer discrepancies must be recorded.
- The system must provide replenishment reports.

---

# 5.7 QUALITY MANAGEMENT

## 5.7.1 Business Objective

Ensure that incoming and outgoing products comply with company quality requirements.

## 5.7.2 Quality Inspection Scenarios

### Incoming Inspection

The company requires inspection for selected product categories.

Inspection parameters:

- Quantity verification.
- Packaging condition.
- Product appearance.
- Lot identification.
- Expiration date validity.
- Product specification compliance.

### Outgoing Inspection

Before dispatch, selected products must undergo verification.

Inspection parameters:

- Correct product.
- Correct quantity.
- Correct lot.
- Acceptable packaging condition.
- Customer-specific requirements.

## 5.7.3 Business Requirements

| ID | Requirement |
|---|---|
| BR-QUA-001 | The system must support incoming quality inspections. |
| BR-QUA-002 | The system must support outgoing quality inspections. |
| BR-QUA-003 | The system must record inspection results. |
| BR-QUA-004 | The system must support pass/fail decisions. |
| BR-QUA-005 | Rejected products must be segregated. |
| BR-QUA-006 | Quality records must be traceable to source documents. |
| BR-QUA-007 | Quality defects must be reportable. |

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

- Delivery orders must be linked to sales orders.
- Delivery addresses must be configurable.
- Partial shipments must be supported.
- Delivery status must be traceable.
- Proof of delivery must be recorded.
- Delivery discrepancies must be documented.
- Shipping costs must be recorded.
- Customer delivery performance must be measurable.

## 5.8.4 Delivery Performance KPIs

The company will monitor:

- On-Time Delivery Rate.
- Order Fulfillment Rate.
- Delivery Accuracy.
- Average Delivery Lead Time.
- Partial Delivery Rate.
- Failed Delivery Rate.

Advanced route optimization and vehicle tracking are not included in the initial implementation.

---

# 5.9 RETURNS AND REVERSE LOGISTICS

## 5.9.1 Business Objective

Establish standardized processes for handling customer returns and supplier returns.

## 5.9.2 Customer Return Scenarios

Common return reasons include:

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

- Return requests must be documented.
- Return reasons must be categorized.
- Returns must reference original transactions.
- Returned goods must undergo inspection.
- Return quantities must be traceable.
- Credit notes must be supported.
- Supplier replacement goods must be traceable.
- Return performance must be reportable.

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
3. Customer invoice is generated according to the company's invoicing policy.
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

## 5.10.4 Three-Way Matching

The company requires a three-way matching control between:

1. Purchase Order.
2. Goods Receipt.
3. Vendor Bill.

Example:

| Document | Quantity | Unit Price |
|---|---:|---:|
| Purchase Order | 1,000 | IDR 2,500 |
| Goods Receipt | 1,000 | IDR 2,500 |
| Vendor Bill | 1,000 | IDR 2,500 |

Expected result:

The system must identify discrepancies between ordered, received, and invoiced quantities and values.

Exceptions must be reviewed by authorized Finance or Procurement personnel.

## 5.10.5 Tax Management

The company operates in Indonesia and requires configurable tax handling.

The implementation must consider:

- Applicable VAT/PPN.
- Tax-inclusive and tax-exclusive pricing.
- Input tax.
- Output tax.
- Tax invoice references.
- Tax reporting requirements.

Actual tax rates and accounting treatment must be confirmed against applicable Indonesian regulations during implementation.

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

Ensure that imported products reflect their actual acquisition costs, including additional procurement and logistics expenses.

## 5.11.2 Landed Cost Components

The company imports selected products from international suppliers.

Applicable cost components may include:

- International freight.
- Insurance.
- Customs-related charges.
- Port handling.
- Customs brokerage.
- Domestic transportation.
- Other eligible acquisition costs.

## 5.11.3 Example Scenario

An import purchase is made from Shenzhen Trading Co.

| Cost Component | Amount |
|---|---:|
| Product Purchase Value | IDR 100,000,000 |
| International Freight | IDR 8,000,000 |
| Insurance | IDR 1,000,000 |
| Customs and Import Charges | IDR 12,000,000 |
| Port Handling | IDR 2,000,000 |
| Domestic Transportation | IDR 3,000,000 |
| Total Acquisition Cost | IDR 126,000,000 |

The system must support the allocation of eligible landed costs to received inventory using an approved allocation method.

Possible allocation methods:

- Equal.
- By quantity.
- By current cost.
- By weight.
- By volume.

The selected allocation method must reflect the actual cost structure.

---

# 5.12 VENDOR PERFORMANCE MANAGEMENT

## 5.12.1 Business Objective

Provide measurable supplier evaluation to support procurement decisions.

## 5.12.2 Vendor Evaluation Criteria

| KPI | Measurement |
|---|---|
| On-Time Delivery | Percentage of deliveries received on schedule |
| Order Fulfillment | Percentage of ordered quantities delivered |
| Quality Acceptance | Percentage of accepted products |
| Price Competitiveness | Comparison against historical and alternative vendor pricing |
| Lead Time Reliability | Actual versus promised delivery lead time |

## 5.12.3 Example Vendor Evaluation

| KPI | Target | Actual |
|---|---:|---:|
| On-Time Delivery | 95% | 92% |
| Order Fulfillment | 98% | 97% |
| Quality Acceptance | 99% | 98% |

The system must provide vendor performance visibility to the Procurement Department.

The evaluation must be based on actual historical transaction data rather than manually entered ratings alone.

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

Customer segmentation must be based on approved business criteria such as sales volume, profitability, and commercial agreements.

---

# 5.14 APPROVAL AND INTERNAL CONTROL

## 5.14.1 Business Objective

Establish accountability and prevent unauthorized business transactions.

## 5.14.2 Approval Requirements

The system must support controlled approvals for:

- Purchase orders.
- Sales discounts.
- Customer credit exceptions.
- Inventory adjustments.
- Stock write-offs.
- Supplier returns.
- Customer refunds.
- Exceptional pricing.

## 5.14.3 Segregation of Duties

The company requires separation between transaction preparation, review, approval, and execution.

Example:

| Process | Responsible Role | Approval Role |
|---|---|---|
| Purchase Requisition | Procurement Staff | Procurement Supervisor |
| Purchase Order | Procurement Officer | Authorized Manager |
| Inventory Adjustment | Warehouse Staff | Warehouse Manager |
| Credit Exception | Sales Staff | Finance Manager |
| Customer Refund | Customer Service | Finance Manager |
| Vendor Payment | Accounts Payable | Finance Manager |

A user must not be able to approve their own transaction when the relevant segregation-of-duties policy prohibits it.

## 5.14.4 Audit Trail

The system must maintain:

- Document creation history.
- Document modification history.
- Approval history.
- Transaction status changes.
- Inventory movement history.
- User activity references.
- Relevant financial transaction references.

---

# 5.15 MANAGEMENT REPORTING AND BUSINESS INTELLIGENCE

## 5.15.1 Business Objective

Provide management with reliable operational and financial insights.

## 5.15.2 Required Management Dashboards

### Inventory Dashboard

- Total inventory quantity.
- Total inventory valuation.
- Stock availability.
- Below-minimum stock.
- Overstocked products.
- Near-expiration products.
- Expired products.
- Inventory aging.
- Warehouse stock comparison.

### Sales Dashboard

- Total sales revenue.
- Sales by customer.
- Sales by product.
- Sales by territory.
- Sales by salesperson.
- Sales order fulfillment.
- Outstanding customer invoices.
- Sales return analysis.

### Procurement Dashboard

- Total purchasing value.
- Purchase orders by vendor.
- Purchase orders by status.
- Vendor delivery performance.
- Purchase price trends.
- Outstanding purchase orders.
- Procurement lead time.

### Warehouse Dashboard

- Incoming goods volume.
- Outgoing goods volume.
- Picking productivity.
- Packing productivity.
- Inventory discrepancies.
- Stock transfer performance.
- Return processing volume.

### Financial Dashboard

- Accounts receivable.
- Accounts payable.
- Overdue receivables.
- Cash and bank balances.
- Gross profit.
- Inventory valuation.
- Profit and loss.

## 5.15.3 Reporting Requirements

- Reports must support date filtering.
- Reports must support warehouse filtering.
- Reports must support product category filtering.
- Reports must support customer and vendor filtering.
- Reports must provide export capabilities where appropriate.
- Financial reports must use validated accounting data.
- Management dashboards must reflect the underlying transactional records.

---

# 6. END-TO-END BUSINESS SCENARIOS

This section defines the integrated business scenarios that must be demonstrated during implementation.

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
7. Finance processes credit note.
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

**Expected outcome:** Imported product costs accurately reflect eligible acquisition expenses.

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

**Expected outcome:** Supplier evaluation is based on operational evidence.

---

# 7. NON-FUNCTIONAL REQUIREMENTS

## 7.1 Performance

- Normal business transactions should respond within an acceptable operational timeframe.
- Standard form operations should target a response time of approximately 3 seconds under the agreed test environment.
- Management reports should execute within acceptable business reporting windows.
- Database queries should be optimized for expected transaction volumes.
- Batch operations must avoid unnecessary performance degradation.

Performance targets must be validated through realistic testing rather than assumed from development environments.

## 7.2 Security

- User authentication must be required.
- Access must be role-based.
- Sensitive financial information must be restricted.
- Warehouse users must only access authorized operational areas.
- Approval permissions must be separated from normal transaction permissions.
- Unauthorized record modification must be prevented.
- User activities must be traceable.

## 7.3 Availability

- The system must support normal business operating hours.
- Database backup procedures must be established.
- Recovery procedures must be documented.
- System failures must be logged.
- Deployment must support service restart and recovery.

## 7.4 Data Integrity

- Master data must maintain unique references.
- Transactions must maintain valid relationships.
- Inventory movements must remain traceable.
- Financial transactions must preserve accounting integrity.
- Deleted or cancelled business documents must not silently corrupt historical records.

## 7.5 Scalability

The system architecture must accommodate:

- Additional warehouses.
- More customers and suppliers.
- Larger product catalogs.
- Increased transaction volumes.
- Additional business users.
- Future custom modules.

## 7.6 Usability

- Interfaces must be understandable to operational users.
- Standardized naming conventions must be applied.
- Forms must provide meaningful validation.
- Reports must use clear business terminology.
- Users must receive appropriate training.

---

# 8. USER ROLES AND RESPONSIBILITIES

The ERP system must support role-based access control.

| Role | Main Responsibilities |
|---|---|
| System Administrator | Technical system configuration |
| ERP Manager | Functional administration |
| Sales Representative | Customer quotations and sales |
| Sales Manager | Sales supervision and approvals |
| Procurement Officer | Supplier sourcing and purchasing |
| Procurement Manager | Procurement approval |
| Warehouse Operator | Receiving, picking, packing |
| Warehouse Supervisor | Warehouse supervision |
| Inventory Controller | Stock reconciliation and reporting |
| Quality Inspector | Product inspections |
| Logistics Coordinator | Shipment coordination |
| Customer Service | Customer complaints and returns |
| Accounts Receivable | Customer invoicing and collection |
| Accounts Payable | Supplier invoices and payments |
| Finance Manager | Financial control and approval |
| Managing Director | Executive oversight |

Access permissions must be configured according to the principle of least privilege.

---

# 9. MASTER DATA AND PORTFOLIO DATASET

## 9.1 Initial Dummy Data Volume

The following dataset will be used for portfolio implementation.

| Data Entity | Target Records |
|---|---:|
| Products | 500 |
| Product Categories | 5 |
| Customers | 250 |
| Vendors | 40 |
| Warehouses | 3 |
| Internal Locations | 30 |
| Sales Users | 10 |
| Procurement Users | 5 |
| Warehouse Users | 12 |
| Finance Users | 5 |
| Historical Sales Orders | 1,000 |
| Historical Purchase Orders | 300 |
| Initial Inventory Lots | 100 |
| Initial Stock Quantities | 500+ |

These figures are implementation targets, not claims of actual company data.

## 9.2 Sample Sales Transaction

| Attribute | Value |
|---|---|
| Sales Order | SO-2026-0001 |
| Customer | PT Retail Makmur |
| Warehouse | WH-JKT |
| Order Date | 12-Nov-2026 |
| Product | Arunika Mineral Water 600ml |
| Quantity | 1,000 Units |
| Unit Price | IDR 3,500 |
| Subtotal | IDR 3,500,000 |
| Tax | According to configured tax policy |
| Payment Terms | Net 30 |

## 9.3 Sample Purchase Transaction

| Attribute | Value |
|---|---|
| Purchase Order | PO-2026-0001 |
| Vendor | PT Nusantara Food Supply |
| Warehouse | WH-JKT |
| Order Date | 12-Nov-2026 |
| Product | Arunika Mineral Water 600ml |
| Quantity | 5,000 Units |
| Unit Price | IDR 2,500 |
| Subtotal | IDR 12,500,000 |
| Expected Lead Time | 7 Days |

## 9.4 Data Migration Requirements

Although the portfolio uses dummy data, the implementation must demonstrate realistic migration practices.

Requirements:

- Data templates must be prepared.
- Product references must be validated.
- Customer and vendor records must be checked for duplicates.
- Opening inventory must be reconciled.
- Lot and expiration information must be validated.
- Opening financial balances must be reconciled.
- Data migration results must be documented.

---

# 10. BUSINESS KPI AND SUCCESS CRITERIA

The project will use measurable KPIs to evaluate business improvements.

The following targets are fictional portfolio acceptance targets and will require baseline measurement during implementation.

| KPI ID | KPI | Target |
|---|---|---:|
| KPI-001 | Inventory Accuracy | ≥ 98% |
| KPI-002 | On-Time Delivery Rate | ≥ 95% |
| KPI-003 | Order Fulfillment Rate | ≥ 97% |
| KPI-004 | Supplier On-Time Delivery | ≥ 95% |
| KPI-005 | Purchase Order Processing Time | ≤ 1 business day after complete approval request |
| KPI-006 | Sales Order Processing Time | ≤ 15 minutes for standard orders |
| KPI-007 | Expired Product Sales | 0 |
| KPI-008 | Stock Traceability | 100% for tracked products |
| KPI-009 | Inventory Reconciliation Completion | 100% of scheduled counts |
| KPI-010 | Financial Reconciliation Accuracy | 100% of validated test cases |

## 10.1 KPI Measurement Method

Inventory Accuracy:

Physical inventory quantity compared against recorded system inventory.

On-Time Delivery Rate:

Orders delivered within the agreed delivery date divided by total eligible delivered orders.

Order Fulfillment Rate:

Quantity delivered divided by quantity ordered, measured for completed delivery commitments.

Supplier On-Time Delivery:

Purchase receipts received on or before the agreed delivery date divided by eligible purchase receipts.

Expired Product Sales:

Number of expired products included in validated outbound sales deliveries.

Stock Traceability:

Percentage of tracked inventory transactions with complete lot or serial identification.

---

# 11. ASSUMPTIONS AND DEPENDENCIES

## 11.1 Business Assumptions

1. The company operates under a single legal entity for the initial implementation.
2. All three warehouses belong to the same company.
3. The business primarily operates using IDR.
4. The company uses B2B sales processes.
5. Product traceability is required for selected products.
6. The company uses customer credit terms.
7. Procurement includes domestic and international suppliers.
8. Inventory valuation follows an approved accounting policy.
9. Each department provides designated ERP users.
10. All dummy transactions are created for portfolio demonstration.

## 11.2 Technical Assumptions

1. Odoo 19 Enterprise is installed and operational.
2. PostgreSQL is available.
3. Ubuntu Linux is used for deployment.
4. Required Enterprise applications are licensed and accessible.
5. Custom modules will follow Odoo development conventions.
6. External integrations will use documented APIs.
7. Database backup and recovery procedures will be established.
8. Development and testing will use separate environments where practical.

## 11.3 Dependencies

- Business approval of requirements.
- Availability of master data.
- Approved accounting policies.
- Approved warehouse procedures.
- Defined user roles.
- Odoo Enterprise application availability.
- Tax configuration confirmation.
- Valid dummy datasets.
- Acceptance of test scenarios.

---

# 12. PROJECT RISKS AND MITIGATION

| Risk ID | Risk | Potential Impact | Mitigation |
|---|---|---|---|
| RSK-001 | Inconsistent master data | Incorrect transactions | Data cleansing and validation |
| RSK-002 | Incorrect inventory opening balances | Inventory discrepancies | Opening stock reconciliation |
| RSK-003 | Incorrect accounting configuration | Financial reporting errors | Finance review and testing |
| RSK-004 | Poor user adoption | Operational disruption | User training |
| RSK-005 | Incorrect access permissions | Unauthorized activities | Security testing |
| RSK-006 | Inadequate warehouse procedures | Fulfillment errors | Standardized SOP |
| RSK-007 | Custom module defects | Business process failures | Automated and manual testing |
| RSK-008 | Poor integration reliability | Inconsistent external data | Error handling and retry mechanisms |
| RSK-009 | Performance degradation | Slow transactions | Load and performance testing |
| RSK-010 | Insufficient backup procedures | Data loss | Backup and recovery testing |
| RSK-011 | Incorrect lot/expiration data | Product traceability failure | Receiving validation |
| RSK-012 | Inaccurate landed cost allocation | Incorrect inventory valuation | Financial reconciliation |

---

# 13. IMPLEMENTATION SUCCESS AND ACCEPTANCE CRITERIA

The implementation will be considered functionally successful when the following conditions are achieved:

## 13.1 Functional Acceptance

- Master data can be created and maintained.
- Sales quotations can be converted into sales orders.
- Customer credit controls operate according to approved policies.
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
- Management reports provide consistent transactional information.

## 13.2 Technical Acceptance

- Custom modules install without critical errors.
- Custom models and business logic behave as specified.
- Access controls prevent unauthorized transactions.
- Required automated jobs execute successfully.
- APIs handle valid and invalid requests appropriately.
- Automated tests pass.
- Database backup and recovery are demonstrated.
- Deployment documentation is available.

## 13.3 Operational Acceptance

- Users can execute assigned business processes.
- Standard operating procedures are documented.
- Training materials are available.
- Critical business scenarios are successfully tested.
- No unresolved critical defects remain.
- UAT approval is documented.

---

# 14. REQUIREMENTS PRIORITIZATION

Requirements will be prioritized using the MoSCoW method.

| Priority | Definition |
|---|---|
| Must Have | Mandatory for core business operation |
| Should Have | Important, but temporary workaround may exist |
| Could Have | Useful enhancement that can be deferred |
| Won't Have | Explicitly excluded from current implementation |

The requirements marked Must Have form the baseline for initial functional acceptance.

---

# 15. GLOSSARY

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

---

# 16. BRD CONCLUSION

The Advanced Wholesale Distribution & Supply Chain ERP implementation aims to transform PT Arunika Distribusi Nusantara from fragmented operational management into an integrated, centralized, and controlled enterprise distribution environment.

The implementation will establish standardized business processes across procurement, warehouse operations, inventory management, sales, logistics, accounting, and supplier management.

Odoo 19 Enterprise will serve as the central ERP platform, supported by appropriate configuration, automation, custom module development, and system integration.

The project will demonstrate a realistic enterprise distribution environment and provide evidence of functional consulting, technical development, process integration, and ERP implementation capabilities.

The approved BRD will serve as the baseline reference for subsequent project deliverables.

---

# 17. NEXT DOCUMENTS AND PROJECT DELIVERABLES

The following documents will be developed using this BRD as the business requirements baseline.

| Sequence | Document | Purpose |
|---|---|---|
| 01 | Business Requirements Document (BRD) | Defines business needs and processes |
| 02 | Scope of Work (SOW) | Defines implementation boundaries and deliverables |
| 03 | Functional Specification Document (FSD) | Defines functional behavior and workflows |
| 04 | Technical Design Document (TDD) | Defines architecture and technical implementation |
| 05 | Configuration & Development Guide | Documents actual Odoo implementation |
| 06 | Test Strategy & Test Cases | Defines testing coverage |
| 07 | Test Execution Evidence | Documents test results |
| 08 | Requirements Traceability Matrix | Connects requirements to implementation and tests |
| 09 | UAT & Defect Summary | Records user acceptance and defects |
| 10 | Deployment & Handover Guide | Documents production-like deployment |

## DOCUMENT END

**Document ID:** ADN-BRD-001  
**Project:** Advanced Wholesale Distribution & Supply Chain ERP  
**Organization:** PT Arunika Distribusi Nusantara  
**ERP Platform:** Odoo 19 Enterprise  
**Version:** 1.0  
**Status:** Draft for Baseline