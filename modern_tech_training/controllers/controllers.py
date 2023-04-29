# -*- coding: utf-8 -*-
# from odoo import http


# class ChiliTraining(http.Controller):
#     @http.route('/modern_tech_training/modern_tech_training/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modern_tech_training/modern_tech_training/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('modern_tech_training.listing', {
#             'root': '/modern_tech_training/modern_tech_training',
#             'objects': http.request.env['modern_tech_training.modern_tech_training'].search([]),
#         })

#     @http.route('/modern_tech_training/modern_tech_training/objects/<model("modern_tech_training.modern_tech_training"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modern_tech_training.object', {
#             'object': obj
#         })
