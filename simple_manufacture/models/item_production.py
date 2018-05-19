# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
from openerp.exceptions import ValidationError


class ItemProduction(models.Model):
    _name = 'item.production'
    _description = 'Item Production'

    name = fields.Char(string='Item Name')
    date_start = fields.Datetime(string='Date Start')
    date_finish = fields.Datetime()
    est_date_finish = fields.Datetime(store=False)
    production_detail_ids = fields.One2many('item.production.detail', inverse_name='production_id')

    @api.constrains('production_detail_ids')
    def _check_production_detail_ids(self):
        """
        Condition check before writing documents.
        """
        if not self.check_duplicate_component():
            err_msg = _('There are duplicated component selected.')
            raise ValidationError(err_msg)

        if not self.count_sum_percent_weights() == 100:
            err_msg = _('Total Weights (%) is not equal to 100%')
            raise ValidationError(err_msg)

    def count_sum_percent_weights(self):
        """
        Count sum of percent_weights for all selected components.
        """
        sum_weights = 0
        for component in self.production_detail_ids:
            sum_weights += component.percent_weights
        return sum_weights

    def check_duplicate_component(self):
        """
        Check if there is duplicate component selected.
        """
        component_ids = []
        for component in self.production_detail_ids:
            component_ids.append(component.component_id.id)

        if component_ids:
            unique = set(component_ids)
            for item in unique:
                count = component_ids.count(item)
                if count > 1:
                    return False
        return True


class ItemProductionDetail(models.Model):
    _name = 'item.production.detail'
    _description = 'Item Production Detail'

    production_id = fields.Many2one('item.production', ondelete='cascade', required=True)
    component_id = fields.Many2one('master.component', 'Component Name', required=True)
    percent_weights = fields.Float('Percent Weight', required=True)
