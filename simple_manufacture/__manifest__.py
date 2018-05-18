# -*- coding: utf-8 -*-
{
    'name': "simple_manufacture",

    'summary': """
        Simple manufacture for item and components.""",

    'description': """
        Just a simple manufacture for item and components.
    """,

    'author': "Ardian",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/master_component_views.xml',
        'views/item_production_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}