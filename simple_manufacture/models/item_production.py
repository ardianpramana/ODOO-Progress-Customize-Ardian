# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ItemProduction(models.Model):
    _name = 'item.production'
    _description = 'Item Production'

    name = fields.Char(string='Item Name')
    date_start = fields.Datetime(string='Date Start')
    date_finish = fields.Datetime()
    est_date_finish = fields.Datetime(stored=False)
    production_detail_ids = fields.One2many('item.production.detail', inverse_name='production_id')

#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class ItemProductionDetail(models.Model):
    _name = 'item.production.detail'
    _description = 'Item Production Detail'

    production_id = fields.Many2one('item.production', ondelete='cascade')
    component_ids = fields.Many2one('master.component', 'Component Name')
    percent_weights = fields.Float('Percent Weight')
