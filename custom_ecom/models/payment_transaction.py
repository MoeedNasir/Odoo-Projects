# -*- coding: utf-8 -*-
from odoo import api, fields, models

class CustomPaymentTransaction(models.Model):
    _name = "custom.payment.transaction"
    _description = "E-commerce Payment Transaction"
    _order = "date desc"

    name = fields.Char(string="Transaction Reference", required=True, copy=False, readonly=True, default="New")
    provider = fields.Selection([
        ("stripe", "Stripe"),
        ("paypal", "PayPal"),
    ], required=True, default="stripe")
    transaction_id = fields.Char(string="Transaction ID")
    amount = fields.Float(string="Amount", required=True)
    currency_id = fields.Many2one("res.currency", string="Currency", required=True, default=lambda self: self.env.company.currency_id.id)
    state = fields.Selection([
        ("draft", "Draft"),
        ("done", "Done"),
        ("cancel", "Cancelled"),
        ("error", "Error"),
    ], default="draft", string="Status")
    date = fields.Datetime(default=fields.Datetime.now, string="Date")
    order_id = fields.Many2one("sale.order", string="Related Order")
    journal_entry_id = fields.Many2one("account.move", string="Accounting Entry")

    @api.model
    def create_journal_entry(self, vals):
        journal = self.env["account.journal"].search([("type", "=", "bank")], limit=1)
        if not journal:
            raise ValueError("No bank journal found for payment recording.")

        move = self.env["account.move"].create({
            "move_type": "entry",
            "journal_id": journal.id,
            "ref": vals.get("transaction_id", "Stripe Transaction"),
            "line_ids": [
                (0, 0, {
                    "name": "Payment received from Stripe",
                    "account_id": journal.default_account_id.id,
                    "credit": vals["amount"],
                    "debit": 0.0,
                }),
                (0, 0, {
                    "name": "Customer Receivable",
                    "account_id": self.env.company.account_receivable_id.id,
                    "credit": 0.0,
                    "debit": vals["amount"],
                }),
            ]
        })
        move.action_post()
        return move
