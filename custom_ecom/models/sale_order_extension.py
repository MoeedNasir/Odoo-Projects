# -*- coding: utf-8 -*-
from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_provider = fields.Selection([
        ("stripe", "Stripe"),
        ("paypal", "PayPal"),
    ], string="Payment Provider")
    payment_status = fields.Selection([
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ], default="pending")
    external_payment_id = fields.Char("External Payment ID")
    invoice_created = fields.Boolean("Invoice Created", default=False)
    account_move_id = fields.Many2one("account.move", string="Related Invoice")
