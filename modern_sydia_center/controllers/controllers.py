# -*- coding: utf-8 -*-
# from odoo import http


# class ModernSydiaCenter(http.Controller):
#     @http.route('/modern_sydia_center/modern_sydia_center/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modern_sydia_center/modern_sydia_center/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('modern_sydia_center.listing', {
#             'root': '/modern_sydia_center/modern_sydia_center',
#             'objects': http.request.env['modern_sydia_center.modern_sydia_center'].search([]),
#         })

#     @http.route('/modern_sydia_center/modern_sydia_center/objects/<model("modern_sydia_center.modern_sydia_center"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modern_sydia_center.object', {
#             'object': obj
#         })
