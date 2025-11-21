# -*- coding: utf-8 -*-
{
    "name": "Custom E-commerce",
    "version": "1.0.0",
    "author": "Moeed Nasir",
    "category": "Website/E-commerce",
    "summary": "Custom e-commerce module with payment gateway integration",
    "description": """
        Custom Odoo e-commerce module with product filtering, payment gateway
        integration (Stripe/PayPal), and accounting automation.
    """,
    "depends": ["base", "website", "website_sale", "account", "payment"],
    "data": [
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/product_brand_views.xml",
        "views/payment_gateway_views.xml",
        "views/payment_transaction_views.xml",
        "views/templates/payment_templates.xml",
        "views/templates/website_shop_inherit.xml",
    ],
    "assets": {
        "website.assets_frontend": [
            "/custom_ecom/static/src/js/product_filter.js",
            "/custom_ecom/static/src/scss/style.scss",
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
