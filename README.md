# Inventory Wholesale Distribution ERP

**An Enterprise-Grade Wholesale Distribution & Supply Chain Management Solution Built on Odoo 19 Enterprise**

<p align="center">

![Odoo](https://img.shields.io/badge/Odoo-19%20Enterprise-714B67?style=for-the-badge&logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

![Project Status](https://img.shields.io/badge/Status-Design%20%26%20Development%20Preparation-orange)
![License](https://img.shields.io/badge/License-LGPL--3-blue.svg)
![Documentation](https://img.shields.io/badge/Documentation-Available-success)

</p>

## Overview

**Inventory Wholesale Distribution ERP** is an enterprise ERP implementation project designed for a B2B wholesale distribution business operating across multiple warehouses.

Built on **Odoo 19 Enterprise**, the solution aims to streamline end-to-end business operations, covering customer relationship management, sales, procurement, inventory management, warehouse operations, supply chain planning, accounting, and management reporting.

The project emphasizes business process standardization, configurable approval workflows, inventory traceability, financial control, and operational visibility.

It combines standard Odoo capabilities with purpose-built custom addons to address business-specific requirements that cannot be adequately handled through standard configuration alone.

The solution follows a configuration-first approach while maintaining Odoo's standard transaction models as the primary system of record.

## Business Context

This project uses a fictional wholesale distribution company:

**PT Arunika Distribusi Nusantara (ADN)**

| Business Attribute | Description |
|---|---|
| Industry | FMCG & Consumer Goods Distribution |
| Business Model | B2B Wholesale Distribution |
| ERP Platform | Odoo 19 Enterprise |
| Deployment | On-Premise |
| Operating System | Ubuntu Linux |
| Database | PostgreSQL |
| Primary Currency | Indonesian Rupiah (IDR) |
| Legal Entity | Single Company |
| Warehouses | 3 |
| Product Catalog | 500 SKUs |
| Customers | 250 |
| Vendors | 40 |
| User Role Staging | 20 Records |

### Warehouse Structure

| Warehouse | Code | Primary Responsibility |
|---|---|---|
| Jakarta Central Warehouse | WH-JKT | Central receiving, supplier/import handling, and inventory allocation |
| Bandung Regional Warehouse | WH-BDG | West Java distribution and fulfillment |
| Surabaya Regional Warehouse | WH-SBY | East Java distribution and regional inventory management |

## Key Business Capabilities

### 1. Master Data Management

- Centralized product and product category management.
- Customer and vendor management.
- Multiple delivery and invoice addresses.
- Product and vendor-specific purchasing information.
- Units of measure management.
- Warehouse and internal location hierarchy.
- Lot, serial number, and expiration date configuration.
- Controlled master data creation and amendment.

### 2. Customer Relationship Management (CRM)

- Lead and opportunity management.
- Sales pipeline tracking.
- Salesperson and sales team assignment.
- Customer activity and follow-up management.
- Opportunity conversion into quotations.
- Customer segmentation based on annual net sales.
- Controlled strategic customer segment override.

### 3. Sales Management

- Customer-specific pricelists.
- Quotation and sales order management.
- Discount approval per sales order line.
- Exceptional pricing justification.
- Customer credit exposure validation.
- Credit hold and exception release.
- Stock reservation and fulfillment.
- Partial delivery management.
- Customer invoicing and payment reconciliation.

### 4. Procurement Management

- Replenishment-driven purchasing demand.
- Internal purchase request process.
- Request for Quotation (RFQ) management.
- Vendor quotation comparison.
- Purchase order approval by value.
- Multi-level approval workflow.
- Automatic re-evaluation after purchase order amendments.
- Partial and complete goods receiving.
- Incoming quality inspection.
- Purchase order, receipt, and vendor bill matching.
- Vendor payment management.

### 5. Inventory Management

- Multi-warehouse inventory management.
- Hierarchical warehouse locations.
- Real-time inventory visibility.
- Lot and serial number tracking.
- Expiration date management.
- FEFO (First Expired, First Out).
- FIFO and AVCO costing methods.
- Automated inventory valuation.
- Inventory adjustment approval.
- Cycle counting and stock reconciliation.
- Inventory aging and shelf-life monitoring.

### 6. Warehouse Management

- Inbound receiving operations.
- Quality inspection and quarantine.
- Putaway operations.
- Internal stock movements.
- Picking and packing.
- Outbound delivery processing.
- Barcode-enabled warehouse operations, subject to application and device availability.
- Proof of Delivery (POD) reference management.
- Delivery discrepancy tracking.

### 7. Supply Chain Management

- Warehouse-specific replenishment rules.
- Minimum and maximum stock policies.
- Inter-warehouse transfers.
- Internal transit locations.
- Partial transfer receiving.
- Vendor lead time management.
- Supply availability monitoring.
- Inventory allocation and stock movement traceability.

### 8. Quality Management

- Incoming quality inspection.
- Quality control points.
- Quality check records.
- Quarantine management.
- Defective stock handling.
- Quality-related vendor performance evaluation.

### 9. Accounting & Financial Management

- Customer invoices and accounts receivable.
- Vendor bills and accounts payable.
- Customer payment registration.
- Vendor payment registration.
- Bank and cash journal configuration.
- Payment reconciliation.
- Credit notes and refunds.
- Inventory valuation accounting.
- Cost of Goods Sold (COGS).
- Financial reporting.

Indonesian localization, tax configuration, chart of accounts, and statutory reporting require validation by qualified Finance and tax reviewers before production use.

### 10. Landed Cost Management

- Additional acquisition cost recording.
- Freight and insurance cost allocation.
- Customs and import-related cost allocation.
- Landed cost distribution to eligible inventory receipts.
- Inventory valuation impact tracking.

### 11. Vendor Performance Management

- Vendor delivery performance.
- Purchase price evaluation.
- Quality performance measurement.
- Vendor reliability indicators.
- Weighted vendor scorecard.
- Vendor performance reporting.

### 12. Management Reporting & Business Intelligence

- Sales performance reporting.
- Purchase performance reporting.
- Inventory availability and aging.
- Warehouse operational performance.
- Vendor performance scorecards.
- Customer credit exposure.
- Financial performance.
- Consolidated management dashboards.

## Custom Addon Architecture

The project follows a modular architecture that separates reusable business controls from transaction-specific implementations.

### Planned Custom Addons

| Addon | Responsibility | Priority |
|---|---|---|
| `adn_approval_core` | Reusable approval engine | Must |
| `adn_purchase_approval` | Purchase order approval | Must |
| `adn_sale_discount_approval` | Sales discount approval | Must |
| `adn_credit_control` | Customer credit exposure and credit holds | Must |
| `adn_inventory_adjustment_approval` | Inventory adjustment approval | Must |
| `adn_refund_approval` | Refund approval and execution control | Must |
| `adn_vendor_scorecard` | Vendor performance evaluation | Must |
| `adn_management_reporting` | Consolidated management dashboards | Should |
| `adn_supply_chain_extensions` | Optional supply chain enhancements | Should |

Additional functional enhancements may be implemented as separate addons where appropriate, including:

- Customer/order shelf-life validation.
- Quality sampling enhancements.
- Delivery discrepancy tracking.
- Stock aging enhancements.

These enhancements remain subject to confirmation that standard Odoo functionality is insufficient.

### Architecture Principles

1. Standard Odoo transaction models remain the system of record.
2. Configuration is preferred over custom development.
3. Business approval policies are configurable and version-controlled.
4. Critical business controls are enforced server-side.
5. Approval history must remain auditable.
6. Custom addons must not create parallel sales, purchase, inventory, or accounting ledgers.
7. Custom modules must respect Odoo security, access rights, and segregation of duties.
8. Customizations must remain maintainable and upgrade-conscious.

## Technical Architecture

The solution follows a layered architecture:

```text
+--------------------------------------------------+
|                 Odoo Web Client                  |
|                                                  |
| Sales | Procurement | Warehouse | Finance       |
+--------------------------------------------------+
                       |
                       v
+--------------------------------------------------+
|              Standard Odoo 19 Enterprise        |
|                                                  |
| CRM | Sales | Purchase | Inventory | Accounting  |
| Quality | Barcode | Contacts | Reporting        |
+--------------------------------------------------+
                       |
                       v
+--------------------------------------------------+
|                  ADN Custom Addons               |
|                                                  |
| Approval Core                                    |
| Purchase Approval                                |
| Sales Discount Approval                          |
| Credit Control                                   |
| Inventory Adjustment Approval                   |
| Refund Approval                                  |
| Vendor Scorecard                                 |
| Management Reporting                             |
| Supply Chain Extensions                          |
+--------------------------------------------------+
                       |
                       v
+--------------------------------------------------+
|                    PostgreSQL                    |
|                                                  |
| Standard Odoo Data                               |
| Custom Business Rules                            |
| Approval Requests and Audit History              |
| Vendor Scorecard Results                         |
+--------------------------------------------------+
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Odoo 19 Enterprise | ERP application platform |
| Python | Backend business logic and custom modules |
| PostgreSQL | Relational database |
| XML | Odoo views, menus, security, and configuration data |
| JavaScript | Frontend extensions when required |
| QWeb | Reporting and document templates |
| Ubuntu Linux | On-premise deployment environment |
| Git & GitHub | Version control and source code management |
| Python Unit Testing | Automated testing |
| Odoo ORM | Business data access and model extensions |

## Repository Structure

The planned repository structure follows a modular Odoo addon organization.

```text
inventory-wholesale-distribution-erp/
│
├── addons/
│   │
│   ├── adn_approval_core/
│   │   ├── models/
│   │   ├── security/
│   │   ├── views/
│   │   ├── data/
│   │   ├── wizards/
│   │   ├── tests/
│   │   ├── __init__.py
│   │   └── __manifest__.py
│   │
│   ├── adn_purchase_approval/
│   ├── adn_sale_discount_approval/
│   ├── adn_credit_control/
│   ├── adn_inventory_adjustment_approval/
│   ├── adn_refund_approval/
│   ├── adn_vendor_scorecard/
│   ├── adn_supply_chain_extensions/
│   └── adn_management_reporting/
│
├── config/
│   └── odoo.conf.example
│
├── docs/
│   ├── 01_business_requirements.md
│   ├── 02_scope_of_work.md
│   ├── 03_business_process_mapping.md
│   ├── 04_fungsional_spesification.md
│   ├── 05_fit_gap_analysis.md
│   ├── 06_technical_design.md
│   └── 07_requirements_traceability_matrix.md
│
├── scripts/
│   ├── install_dependencies.sh
│   └── run_tests.sh
│
├── tests/
│
├── .gitignore
├── LICENSE
└── README.md
```

The directory structure represents the intended project organization. Addons, scripts, and configuration files should be added as their implementation work packages are delivered.

## Installation & Setup

### Prerequisites

Before installing the custom addons, ensure the environment has:

- Ubuntu Linux.
- Python version compatible with the selected Odoo 19 build.
- PostgreSQL compatible with Odoo 19.
- Odoo 19 Enterprise source or installation.
- Required Odoo Enterprise applications and valid entitlements.
- Git.

Exact runtime and dependency versions must be pinned against the selected Odoo 19 build.

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/inventory-wholesale-distribution-erp.git

cd inventory-wholesale-distribution-erp
```

### 2. Configure Odoo

Create or update the Odoo configuration file.

```ini
[options]

addons_path = /path/to/odoo/addons,/path/to/enterprise,/path/to/inventory-wholesale-distribution-erp/addons

admin_passwd = CHANGE_ME

db_host = localhost
db_port = 5432
db_user = odoo
db_password = CHANGE_ME

logfile = /var/log/odoo/odoo.log
```

Use protected credentials and appropriate file permissions. Never commit production passwords or secrets.

### 3. Restart Odoo

```bash
sudo systemctl restart odoo
```

### 4. Install Custom Addons

Install the shared approval framework before its dependent addons.

Recommended installation order:

```text
1. adn_approval_core
2. adn_purchase_approval
3. adn_sale_discount_approval
4. adn_credit_control
5. adn_inventory_adjustment_approval
6. adn_refund_approval
7. adn_vendor_scorecard
8. Optional supply chain extensions
9. adn_management_reporting
```

Installation must follow the actual addon manifest dependencies and approved configuration baseline.

Example installation command:

```bash
./odoo-bin \
    -c /etc/odoo/odoo.conf \
    -d wholesale_distribution_dev \
    -i adn_approval_core \
    --stop-after-init
```

Install dependent addons after their dependencies have been installed and verified.

**Note:** These commands describe the intended installation workflow. They do not imply that all custom addons are already implemented or available in this repository.

## Approval Workflow Framework

A central technical capability is the reusable approval engine.

The conceptual approval lifecycle is:

```text
        Draft
          |
          v
       Submitted
          |
          v
   Pending Approval
          |
       +--+--+
       |     |
       v     v
    Approved Rejected
       |
       v
     Released
       |
       v
    Executed
```

The approval engine is designed to support:

- Configurable approval policies.
- Value-based approval tiers.
- Multiple approval levels.
- Dynamic approver assignment.
- Self-approval prevention.
- Approval delegation where authorized.
- Rejection and resubmission.
- Re-approval after material amendments.
- Immutable approval decision history.
- Server-side execution locks.
- Chatter and audit integration.

### Supported Approval Domains

| Business Process | Approval Control |
|---|---|
| Purchase Order | Value-based multi-level approval |
| Sales Discount | Per-line discount approval |
| Customer Credit | Credit exception approval |
| Inventory Adjustment | Absolute inventory valuation difference |
| Customer Refund | Refund approval and execution lock |

## Testing Strategy

Testing is a fundamental part of the implementation lifecycle.

The project is intended to include:

### Unit Testing

- Model validation.
- Business rule calculation.
- Approval tier determination.
- Credit exposure calculation.
- Vendor scorecard computation.
- Security and access validation.

### Integration Testing

- Purchase approval and PO confirmation.
- Sales discount approval and order confirmation.
- Credit control and sales workflow.
- Inventory adjustment and stock valuation.
- Refund approval and accounting execution.
- Vendor scorecard and source transaction consistency.

### Security Testing

- Unauthorized approval attempts.
- Self-approval prevention.
- Record access restrictions.
- Role-based permissions.
- Segregation of duties.
- Direct RPC/API bypass attempts.

### End-to-End Testing

- Procure to Pay (P2P).
- Order to Cash (O2C).
- Replenishment and Inter-Warehouse Transfer.
- Receiving, Quality, and Putaway.
- Picking, Packing, and Dispatch.
- Returns and Refunds.
- Accounting and Financial Reconciliation.

Tests must be executed in a representative environment, with actual execution results and evidence recorded before acceptance.

## Documentation

The project uses structured ERP implementation documentation to maintain business-to-technical traceability.

| Document | Description |
|---|---|
| BRD | Business Requirements Document |
| SOW | Scope of Work |
| BPM | Business Process Mapping |
| FSD | Functional Specification Document |
| FGA | Fit-Gap Analysis |
| TDD | Technical Design Document |
| RTM | Requirements Traceability Matrix |

These documents establish the functional baseline, technical direction, customization scope, and acceptance traceability.

## Project Roadmap

The implementation follows a controlled delivery lifecycle.

- [x] Business requirements and project scope definition.
- [x] Business process mapping.
- [x] Functional Specification Document.
- [x] Fit-Gap Analysis.
- [x] Technical Design Document.
- [x] Requirements Traceability Matrix.
- [ ] Odoo 19 environment validation.
- [ ] Standard Odoo configuration.
- [ ] Custom addon development.
- [ ] Unit and integration testing.
- [ ] Security and performance testing.
- [ ] Data migration and reconciliation.
- [ ] User Acceptance Testing (UAT).
- [ ] Deployment preparation.
- [ ] Production deployment and operational handover.

The completed checklist items refer to project documentation deliverables, not deployed or tested software functionality.

## Scope Exclusions

The following capabilities are outside the current project baseline unless approved through formal change control:

- Manufacturing and MRP.
- HR and Payroll.
- Full Transportation Management System (TMS).
- Fleet management and live vehicle tracking.
- Advanced route optimization.
- Marketplace integration.
- Banking and payment gateway integration.
- Live carrier API integration.
- Customs brokerage integration.
- Warehouse robotics.
- AI-based demand forecasting.

## Project Documentation & Governance

The project follows these governance principles:

- Requirements must be traceable to functional and technical deliverables.
- Custom development must be justified by an approved fit-gap outcome.
- Business rules must be configurable where appropriate.
- Technical changes must undergo code review and testing.
- Changes to approved requirements must follow formal change control.
- Production releases require backup, deployment, validation, and rollback plans.

## Disclaimer

This repository represents a fictional enterprise ERP implementation portfolio project.

PT Arunika Distribusi Nusantara, its business operations, stakeholders, policies, sample data, and approval thresholds are fictional.

The repository and its documentation do not constitute evidence of an actual client implementation, live production deployment, completed UAT, or statutory compliance certification.

All technical implementation details must be validated against the actual Odoo 19 Enterprise environment before production deployment.

## License

This project is intended to use the **GNU Lesser General Public License v3.0 (LGPL-3)** for original custom addons, subject to the final license and dependency review.

Odoo Enterprise and third-party dependencies remain subject to their respective licenses and commercial terms.

## Author

**ERP Solution Architecture & Development**

Odoo 19 Enterprise | Wholesale Distribution | Supply Chain Management | ERP Customization

---

<p align="center">
  <strong>Designed for operational control, inventory accuracy, financial integrity, and scalable wholesale distribution.</strong>
</p>