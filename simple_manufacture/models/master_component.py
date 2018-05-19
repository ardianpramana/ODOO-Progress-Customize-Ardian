# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
from openerp.exceptions import ValidationError

class MasterComponent(models.Model):
    _name = 'master.component'
    _description = 'Master Component'

    # complete_name = fields.Char()
    name = fields.Char(required=True)
    estimation_time = fields.Float(required=True)

    @api.constrains('name')
    def _check_name(self):
        master_component_ids = self.search([])
        for record in master_component_ids:
            if record.name == self.name:
                err_msg = _('Current component name is already in the master data. '
                            'Please choose another component name!')
                raise ValidationError(err_msg)

