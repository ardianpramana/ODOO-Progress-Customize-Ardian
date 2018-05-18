# -*- coding: utf-8 -*-
from odoo import http

# class Simple-manufacture(http.Controller):
#     @http.route('/simple_manufacture/simple_manufacture/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/simple_manufacture/simple_manufacture/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('simple_manufacture.listing', {
#             'root': '/simple_manufacture/simple_manufacture',
#             'objects': http.request.env['simple_manufacture.simple_manufacture'].search([]),
#         })

#     @http.route('/simple_manufacture/simple_manufacture/objects/<model("simple_manufacture.simple_manufacture"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('simple_manufacture.object', {
#             'object': obj
#         })