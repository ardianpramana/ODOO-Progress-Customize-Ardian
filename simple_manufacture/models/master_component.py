# -*- coding: utf-8 -*-
from datetime import date

from openerp import models, fields, api, exceptions, _
from openerp.exceptions import ValidationError

class MasterComponent(models.Model):
    _name = 'master.component'
    _description = 'Master Component'

    sequence_name = fields.Char(default='New')
    date = fields.Date("Date", default=date.today(), required=True, readonly=True)
    name = fields.Char(required=True)
    estimation_time = fields.Float(required=True)

    # @api.constrains('name')
    # def _check_name(self):\
    #     master_component_ids = self.search([['id', '!=', self.id]])
    #     print master_component_ids
        # for record in master_component_ids:
        #     if record.name == self.name:
        #         err_msg = _('Current component name is already in the master data. '
        #                     'Please choose another component name!')
        #         raise ValidationError(err_msg)

    @api.model
    def create(self, vals):
        """ Get sequence for master_component"""
        if vals.get('sequence_name', 'New') == 'New':
            seq_obj = self.env['ir.sequence']
            vals['sequence_name'] = seq_obj.with_context(ir_sequence_date=vals['date']).next_by_code('master.component') \
                                    or '/'
        return super(MasterComponent, self).create(vals)
