# -*- coding: utf-8 -*-
from odoo.tests.common import HttpCase

class TestProductFilter(HttpCase):
    def test_product_filter_api(self):
        product = self.env['product.template'].create({
            'name': 'Filter Test Product',
            'list_price': 50,
            'website_published': True,
            'sale_ok': True,
        })
        response = self.url_open('/custom_ecom/products', data={
            'filters': {'min_price': 40, 'max_price': 60}
        })
        self.assertEqual(response.status_code, 200)
