# -*- coding: utf-8 -*-
from datetime import date

from openerp import models, fields, api, exceptions, _
from openerp.exceptions import ValidationError

class MasterComponent(models.Model):
    _name = 'master.component'
    _description = 'Master Component'

    sequence_name = fields.Char(default='New')
    name = fields.Char(required=True)
    estimation_time = fields.Integer(required=True)

    @api.constrains('name')
    def _check_name(self):
        master_component_ids = self.search([['id', '!=', self.id]])
        for record in master_component_ids:
            if record.name == self.name:
                err_msg = _('Current component name is already in the master data. '
                            'Please choose another component name!')
                raise ValidationError(err_msg)

    @api.constrains('estimation_time')
    def _check_estimation_time(self):
        if not self.estimation_time > 0:
            err_msg = _('Please input more than 0 days')
            raise ValidationError(err_msg)

    @api.model
    def create(self, vals):
        """ Get sequence for master_component"""
        current_date = date.today().isoformat()
        if vals.get('sequence_name', 'New') == 'New':
            seq_obj = self.env['ir.sequence']
            vals['sequence_name'] = seq_obj.with_context(ir_sequence_date=current_date).next_by_code('master.component') \
                                    or '/'
        return super(MasterComponent, self).create(vals)
