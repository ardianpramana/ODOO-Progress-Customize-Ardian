# -*- coding: utf-8 -*-

from openerp.tests import TransactionCase
from openerp.exceptions import AccessError

class TestSecurity(TransactionCase):

    def setUp(self):
        super(TestSecurity, self).setUp()

        self.MasterComponent_obj = self.env['master.component']
        self.ItemProduction_obj = self.env['item.production']
        self.ItemProductionDetail_obj = self.env['item.production.detail']

        # User
        User = self.env['res.users'].with_context({'no_reset_password': True})
        # group_user = self.ref('simple_manufacture.group_user')
        self.user_no_access = User.create({
            'name': 'No Access', 'login': 'no-user', 'email': 'no.user@user.com'})
        self.user_simple_manufacture = self.env.ref('simple_manufacture.user_component')

        self.vals_master_component_1 = self.MasterComponent_obj.sudo().create({
            'name': 'Lamp',
            'estimation_time': '4',
        })
        self.vals_master_component_2 = self.MasterComponent_obj.sudo().create({
            'name': 'Cable',
            'estimation_time': '2',
        })
        self.vals_master_component_3 = ({
            'name': 'Electric Switch',
            'estimation_time': '2',
        })

        self.vals_item_production = {
            'name': 'Desk Lamp',
            'date_start': '2018-05-21 17:14:39',
            'production_detail_ids': [
                (0, 0, {
                    'component_id': self.vals_master_component_1.id,
                    'percent_weights': '65',
                }),
                (0, 0, {
                    'component_id': self.vals_master_component_2.id,
                    'percent_weights': '35',
                }),
            ],
        }

    def test_00_no_access(self):
        """
        Do not allow user with no group to create data
        """
        # Create
        with self.assertRaises(AccessError):
            self.MasterComponent_obj.sudo(self.user_no_access).create(self.vals_master_component_3)
        with self.assertRaises(AccessError):
            self.ItemProduction_obj.sudo(self.user_no_access).create(self.vals_item_production)

        # write
        self.assertTrue(self.MasterComponent_obj.sudo(self.user_no_access).write({
            'name': 'Electric Switch',
            'estimation_time': '5',
        }))
        self.assertTrue(self.ItemProduction_obj.sudo(self.user_no_access).write({
            'name': 'Desk Lamp',
            'date_start': '2018-05-21 17:14:39',
            'production_detail_ids': [
                (0, 0, {
                    'component_id': self.vals_master_component_1.id,
                    'percent_weights': '100',
                }),
            ],
        }))

        # Unlink
        with self.assertRaises(AccessError):
            self.MasterComponent_obj.sudo(self.user_no_access).search([]).unlink()
        with self.assertRaises(AccessError):
            self.ItemProduction_obj.sudo(self.user_no_access).search([]).unlink()

    def test_01_user_simple_manufacture(self):
        """
        User simple manufacture can create data
        """
        # Create
        self.assertTrue(
            self.MasterComponent_obj.sudo(self.user_simple_manufacture).create(self.vals_master_component_3)
        )
        self.assertTrue(
            self.ItemProduction_obj.sudo(self.user_simple_manufacture).create(self.vals_item_production)
        )

#       # Write
        self.assertTrue(self.MasterComponent_obj.sudo(self.user_simple_manufacture).write({
            'name': 'Electric Switch',
            'estimation_time': '5',
        }))
        self.assertTrue(self.ItemProduction_obj.sudo(self.user_simple_manufacture).write({
            'name': 'Desk Lamp',
            'date_start': '2018-05-21 17:14:39',
            'production_detail_ids': [
                (0, 0, {
                    'component_id': self.vals_master_component_1.id,
                    'percent_weights': '100',
                }),
            ],
        }))

        # Unlink
        self.assertTrue(self.MasterComponent_obj.sudo(self.user_simple_manufacture).search([]).unlink())
        self.assertTrue(self.ItemProduction_obj.sudo(self.user_simple_manufacture).unlink())
