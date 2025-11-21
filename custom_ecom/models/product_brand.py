# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "Product Brand"

    name = fields.Char(required=True)
    description = fields.Text()
    image = fields.Binary("Logo")
    website_url = fields.Char("Website")
    active = fields.Boolean(default=True)
