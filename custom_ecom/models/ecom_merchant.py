# -*- coding: utf-8 -*-
from odoo import models, fields

class EcomMerchant(models.Model):
    _name = "custom_ecom.merchant"
    _description = "E-commerce Payment Merchant Configuration"
    _rec_name = "provider"

    provider = fields.Selection([
        ("stripe", "Stripe"),
        ("paypal", "PayPal"),
    ], required=True)
    api_key = fields.Char("API Key", required=True)
    secret_key = fields.Char("Secret Key", required=True)
    currency_id = fields.Many2one("res.currency", string="Default Currency")
    webhook_secret = fields.Char("Webhook Secret")
    test_mode = fields.Boolean("Test Mode", default=True)
    active = fields.Boolean(default=True)
