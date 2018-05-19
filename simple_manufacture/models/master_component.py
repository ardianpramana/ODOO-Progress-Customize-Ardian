# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MasterComponent(models.Model):
    _name = 'master.component'
    _description = 'Master Component'

    name = fields.Char(string='Component Name')
    estimation_time = fields.Float(string='Estimation Time')
