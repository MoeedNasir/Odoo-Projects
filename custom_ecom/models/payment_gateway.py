# -*- coding: utf-8 -*-
import sys
print(sys.executable)
from odoo import api, fields, models
import stripe

class PaymentGateway(models.Model):
    _name = "payment.gateway"
    _description = "Payment Gateway Configuration"

    name = fields.Char(required=True)
    provider = fields.Selection([
        ("stripe", "Stripe"),
        ("paypal", "PayPal"),
    ], required=True, default="stripe")

    api_key = fields.Char(string="API Secret Key", required=True)
    publishable_key = fields.Char(string="Publishable Key", required=True)
    active = fields.Boolean(default=True)
    test_mode = fields.Boolean(default=True)

    @api.model
    def get_stripe_keys(self):
        gateway = self.search([("provider", "=", "stripe"), ("active", "=", True)], limit=1)
        if not gateway:
            return None
        return {
            "secret_key": gateway.api_key,
            "publishable_key": gateway.publishable_key,
        }
