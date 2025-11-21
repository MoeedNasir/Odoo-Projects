/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ProductFilter = publicWidget.Widget.extend({
    selector: '#filter_panel',
    events: {
        'click #apply_filter': '_onApplyFilter',
    },

    _onApplyFilter() {
        const brand_id = $('#brand_filter').val();
        const min_price = $('#min_price').val();
        const max_price = $('#max_price').val();

        this._rpc({
            route: '/custom_ecom/products',
            params: { filters: { brand_id, min_price, max_price } },
        }).then((data) => {
            const response = JSON.parse(data);
            const products = response.products;
            const grid = $('#products_grid_custom');
            grid.empty();

            products.forEach(prod => {
                grid.append(`<div class="col-lg-3 col-md-4 mb-3">
                    <div class="card p-2">
                        <h6>${prod.name}</h6>
                        <p>$${prod.price}</p>
                        <small>${prod.brand}</small>
                    </div>
                </div>`);
            });
        });
    },
});
publicWidget.registry.StripePaymentButton = publicWidget.Widget.extend({
    selector: '#custom_stripe_btn',

    start() {
        this.el.addEventListener('click', this._onClick.bind(this));
        return this._super(...arguments);
    },

    async _onClick(ev) {
        ev.preventDefault();
        this.el.disabled = true;
        this.el.innerText = 'Processing...';

        try {
            const response = await fetch('/shop/stripe/create_payment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });

            const data = await response.json();
            if (data.client_secret) {
                // Load Stripe library
                const stripe = Stripe(data.publishable_key);
                const result = await stripe.confirmCardPayment(data.client_secret);

                if (result.error) {
                    alert(result.error.message);
                } else if (result.paymentIntent.status === 'succeeded') {
                    window.location.href = '/shop/payment/stripe/success';
                }
            } else {
                alert('Failed to initiate Stripe payment');
            }
        } catch (error) {
            console.error('Stripe error:', error);
            alert('Error while processing payment');
        } finally {
            this.el.disabled = false;
            this.el.innerText = 'Pay Securely with Stripe';
        }
    },
});