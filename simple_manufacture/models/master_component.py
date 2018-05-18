# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MasterComponent(models.Model):
    _name = 'master.component'
    _description = 'Master Component'

    name = fields.Char(string='Component Name')
    estimation_time = fields.Float(string='Estimation Time')
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100