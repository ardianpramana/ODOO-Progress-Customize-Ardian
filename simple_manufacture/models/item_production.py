# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ItemProduction(models.Model):
    _name = 'item.production'
    _description = 'Item Production'

    name = fields.Char(string='Item Name')
    percent_weights = fields.Integer(string='Percent Weights')
    date_start = fields.Date(string='Date Start')
    component_ids = fields.Many2many('master.component')
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100