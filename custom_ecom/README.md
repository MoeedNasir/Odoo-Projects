# Odoo E-commerce + Payment Integration

Custom Odoo e-commerce module integrating payment gateways (Stripe/PayPal) with accounting automation.

## Quick Start (Dev)
```bash
docker compose -f docker-compose.dev.yml up


### Day 2 Progress — Product Filtering & Website Integration

- Added `product.brand` model.
- Implemented JSON-based product search API.
- Added dynamic frontend filters (brand, price).
- Inherited `website_sale.products` template with custom QWeb.
- Integrated JS filtering via `/custom_ecom/products` route.
- Added tests for filter logic.
