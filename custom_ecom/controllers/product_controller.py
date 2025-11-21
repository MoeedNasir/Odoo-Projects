# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class ProductController(http.Controller):

    @http.route(['/custom_ecom/products'], type='json', auth='public', methods=['POST'], csrf=False)
    def fetch_products(self, **kwargs):
        filters = kwargs.get('filters', {})
        domain = [('sale_ok', '=', True), ('website_published', '=', True)]

        if filters.get('brand_id'):
            domain.append(('brand_id', '=', filters['brand_id']))
        if filters.get('category_id'):
            domain.append(('public_categ_ids', 'in', filters['category_id']))
        if filters.get('min_price') and filters.get('max_price'):
            domain += [('list_price', '>=', float(filters['min_price'])),
                       ('list_price', '<=', float(filters['max_price']))]
        if filters.get('rating'):
            domain.append(('rating', '>=', float(filters['rating'])))

        products = request.env['product.template'].sudo().search(domain, limit=20)
        data = [{
            'id': p.id,
            'name': p.name,
            'price': p.list_price,
            'brand': p.brand_id.name or '',
            'rating': p.rating,
        } for p in products]

        return json.dumps({'products': data})
