# -*- coding: utf-8 -*-
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from openerp import models, fields, api, exceptions, _
from openerp.exceptions import ValidationError


class ItemProduction(models.Model):
    _name = 'item.production'
    _description = 'Item Production'

    sequence_name = fields.Char(default='New')
    name = fields.Char(required=True)
    date_start = fields.Datetime(required=True)
    date_finish = fields.Datetime()
    est_date_finish = fields.Datetime(readonly=True, compute='_compute_est_date_finish', store=False)
    production_detail_ids = fields.One2many('item.production.detail', inverse_name='production_id')

    @api.depends('production_detail_ids', 'date_start')
    def _compute_est_date_finish(self):
        """
        Calculate estimated date, based on selected component manufacturing time.
        """
        for rec in self:
            component_time = 0
            # est_date = datetime.today()
            for component in rec.production_detail_ids:
                component_id = self.env['master.component'].search([['id', '=', component.component_id.id]])
                component_time += component_id.estimation_time

            if component_time:
                est_date = (datetime.strptime(rec.date_start, '%Y-%m-%d %H:%M:%S') + relativedelta(days=component_time))
                rec.est_date_finish = est_date.isoformat(' ')

    @api.constrains('production_detail_ids')
    def _check_production_detail_ids(self):
        """
        Condition check before writing documents.
        """
        if not self.production_detail_ids:
            err_msg = _('You have to select component needed.')
            raise ValidationError(err_msg)

        if not self.check_duplicate_component():
            err_msg = _('There are duplicated component selected.')
            raise ValidationError(err_msg)

        if not self.count_sum_percent_weights() == 100:
            err_msg = _('Total Weights (%) is not equal to 100%')
            raise ValidationError(err_msg)

    @api.model
    def create(self, vals):
        """ Get sequence for item_production"""
        current_date = date.today().isoformat()
        if vals.get('sequence_name', 'New') == 'New':
            seq_obj = self.env['ir.sequence']
            vals['sequence_name'] = seq_obj.with_context(ir_sequence_date=current_date).next_by_code('item.production') \
                                    or '/'
        return super(ItemProduction, self).create(vals)

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
    component_id = fields.Many2one('master.component', required=True)
    component_days = fields.Integer(related='component_id.estimation_time', store=False)
    percent_weights = fields.Float('Percent Weight', required=True)
