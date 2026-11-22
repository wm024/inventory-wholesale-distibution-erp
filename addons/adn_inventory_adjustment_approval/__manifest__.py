{
    "name": "ADN Inventory Adjustment Approval",
    "version": "19.0.1.0.1",
    "category": "Inventory/Inventory",
    "summary": "Valuation-based approval gate for standard inventory adjustments",
    "description": (
        "Extends Odoo stock.quant inventory adjustment flow with an auditable "
        "approval request. Standard stock moves and valuation remain authoritative."
    ),
    "author": "Muhammad Ridho Ramadhan",
    "depends": ["stock_account", "mail", "adn_approval_core"],
    "data": [
        "security/inventory_adjustment_groups.xml",
        "security/ir.model.access.csv",
        "data/inventory_adjustment_sequence.xml",
        "data/inventory_adjustment_policy.xml",
        "views/res_company_views.xml",
        "views/stock_quant_views.xml",
        "views/inventory_adjustment_request_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
