from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _update_programs_and_rewards(self):
        """Fix datetime/date comparison in loyalty program"""
        # Call the original method but catch before the problematic line
        res = super(SaleOrder, self)._update_programs_and_rewards()

        # Now apply our fix to the filtered operation
        for order in self:
            order.applied_coupon_ids = order.applied_coupon_ids.filtered(
                lambda c: (not c.expiration_date or
                           c.expiration_date.date() >= fields.Date.today())
            )
        return res