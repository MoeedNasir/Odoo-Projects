# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_featured = fields.Boolean("Featured Product", default=False)
    brand_id = fields.Many2one("product.brand", string="Brand")
    meta_keywords = fields.Char("Meta Keywords")
    meta_description = fields.Text("Meta Description")
    rating = fields.Float("Average Rating", digits=(2, 1))
