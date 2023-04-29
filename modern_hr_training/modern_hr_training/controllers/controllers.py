# -*- coding: utf-8 -*-
# from odoo import http


# class ModernHrTraining(http.Controller):
#     @http.route('/modern_hr_training/modern_hr_training/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modern_hr_training/modern_hr_training/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('modern_hr_training.listing', {
#             'root': '/modern_hr_training/modern_hr_training',
#             'objects': http.request.env['modern_hr_training.modern_hr_training'].search([]),
#         })

#     @http.route('/modern_hr_training/modern_hr_training/objects/<model("modern_hr_training.modern_hr_training"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modern_hr_training.object', {
#             'object': obj
#         })
