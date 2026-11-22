{
    "name": "ADN Purchase Approval",
    "version": "19.0.1.0.1",
    "category": "Purchases",
    "summary": "Tiered, auditable purchase order approval for ADN",
    "description": "Server-side purchase order approval adapter using ADN Approval Core.",
    "author": "Muhammad Ridho Ramadhan",
    "depends": ["purchase", "adn_approval_core"],
    "data": [
        "security/purchase_approval_groups.xml",
        "data/purchase_approval_policy.xml",
        "views/purchase_order_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
