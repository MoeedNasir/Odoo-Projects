# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestEcomModels(TransactionCase):

    def test_create_merchant(self):
        merchant = self.env["custom_ecom.merchant"].create({
            "provider": "stripe",
            "api_key": "test_key",
            "secret_key": "test_secret",
        })
        self.assertTrue(merchant)
        self.assertEqual(merchant.provider, "stripe")
