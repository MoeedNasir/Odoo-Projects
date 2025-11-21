# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import stripe
import logging

_logger = logging.getLogger(__name__)

class StripePaymentController(http.Controller):

    @http.route("/shop/payment/stripe/create", type="json", auth="public", methods=["POST"], csrf=False)
    def create_stripe_session(self, **kw):
        """Create Stripe Checkout session"""
        keys = request.env["payment.gateway"].sudo().get_stripe_keys()
        if not keys:
            return {"error": "Stripe configuration missing"}

        stripe.api_key = keys["secret_key"]

        try:
            # Example data — use actual cart data later
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="payment",
                success_url=request.httprequest.host_url + "shop/payment/success",
                cancel_url=request.httprequest.host_url + "shop/payment/cancel",
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {"name": "Test Product"},
                            "unit_amount": 2000,
                        },
                        "quantity": 1,
                    }
                ],
            )
            return {"sessionId": session.id, "public_key": keys["publishable_key"]}
        except Exception as e:
            _logger.error("Stripe error: %s", str(e))
            return {"error": str(e)}

    @http.route("/shop/payment/success", type="http", auth="public", website=True)
    def payment_success(self, **kw):
        return request.render("custom_ecom.payment_success_template")

    @http.route("/shop/payment/cancel", type="http", auth="public", website=True)
    def payment_cancel(self, **kw):
        return request.render("custom_ecom.payment_cancel_template")

    @http.route("/shop/payment/stripe/confirm", type="json", auth="public", methods=["POST"], csrf=False)
    def confirm_stripe_payment(self, **kw):
        """Confirm payment after success page load."""
        session_id = kw.get("sessionId")
        if not session_id:
            return {"error": "Missing session ID"}

        keys = request.env["payment.gateway"].sudo().get_stripe_keys()
        stripe.api_key = keys["secret_key"]

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == "paid":
                amount = session.amount_total / 100
                transaction = request.env["custom.payment.transaction"].sudo().create({
                    "provider": "stripe",
                    "transaction_id": session.payment_intent,
                    "amount": amount,
                    "currency_id": request.env.company.currency_id.id,
                    "state": "done",
                })

                # Create Journal Entry
                move = transaction.create_journal_entry({
                    "transaction_id": session.payment_intent,
                    "amount": amount,
                })
                transaction.journal_entry_id = move.id

                return {"success": True, "transaction": transaction.name}
            else:
                return {"error": "Payment not confirmed yet."}
        except Exception as e:
            _logger.error("Stripe confirm error: %s", str(e))
            return {"error": str(e)}

class CustomStripeController(http.Controller):

    @http.route('/shop/stripe/create_payment', type='json', auth='public', csrf=False)
    def create_stripe_payment(self):
        """Create Stripe payment intent for website cart order"""
        order = request.website.sale_get_order()
        if not order:
            return {'error': 'No active order'}

        provider = request.env['payment.provider'].sudo().search([('code', '=', 'stripe')], limit=1)
        if not provider:
            return {'error': 'Stripe provider not found'}

        stripe.api_key = provider.stripe_secret_key

        intent = stripe.PaymentIntent.create(
            amount=int(order.amount_total * 100),  # Convert to cents
            currency=order.currency_id.name.lower(),
            metadata={'order_id': order.id}
        )

        return {
            'client_secret': intent.client_secret,
            'publishable_key': provider.stripe_publishable_key
        }

    @http.route('/shop/payment/stripe/success', type='http', auth='public', website=True)
    def stripe_success(self, **kwargs):
        order = request.website.sale_get_order()
        if order:
            order.action_confirm()
        return request.render('custom_ecom.payment_success_template')