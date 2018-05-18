# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
from openerp.exceptions import ValidationError


class ItemProduction(models.Model):
    _name = 'item.production'
    _description = 'Item Production'

    name = fields.Char(string='Item Name')
    date_start = fields.Datetime(string='Date Start')
    date_finish = fields.Datetime()
    est_date_finish = fields.Datetime(stored=False)
    production_detail_ids = fields.One2many('item.production.detail', inverse_name='production_id')
    sum_percent_weights = fields.Float(stored=False)

    @api.constrains('sum_percent_weights')
    def _check_seats_limit(self):
        if self.sum_percent_weights > 100 or self.sum_percent_weights < 100:
            err_msg = _('Total Weights (%) is not equal to 100%')
            raise ValidationError(err_msg)

    @api.onchange('production_detail_ids')
    def _onchange_production_detail_ids(self):
        sum_weights = 0
        for component in self.production_detail_ids:
            sum_weights += component.percent_weights
        self.sum_percent_weights = sum_weights


class ItemProductionDetail(models.Model):
    _name = 'item.production.detail'
    _description = 'Item Production Detail'

    production_id = fields.Many2one('item.production', ondelete='cascade', required=True)
    component_ids = fields.Many2one('master.component', 'Component Name', required=True)
    percent_weights = fields.Float('Percent Weight', required=True)
