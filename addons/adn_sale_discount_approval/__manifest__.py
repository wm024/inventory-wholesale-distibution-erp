{
    "name": "ADN Sales Discount Approval",
    "version": "19.0.1.0.0",
    "category": "Sales",
    "summary": "Per-line discount evaluation and auditable sales approval",
    "description": "Sales order discount approval adapter using ADN Approval Core.",
    "author": "Muhammad Ridho Ramadhan",
    "depends": ["sale_management", "adn_approval_core"],
    "data": [
        "security/sales_discount_groups.xml",
        "data/sales_discount_policy.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
