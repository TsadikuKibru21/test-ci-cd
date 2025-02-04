from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit='sale.order'
    conformed_user_id=fields.Char(string='Conformed User')