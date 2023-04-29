# -*- coding: utf-8 -*-
# from odoo import http


# class ModernAttendanceSummary(http.Controller):
#     @http.route('/modern_attendance_summary/modern_attendance_summary/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modern_attendance_summary/modern_attendance_summary/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('modern_attendance_summary.listing', {
#             'root': '/modern_attendance_summary/modern_attendance_summary',
#             'objects': http.request.env['modern_attendance_summary.modern_attendance_summary'].search([]),
#         })

#     @http.route('/modern_attendance_summary/modern_attendance_summary/objects/<model("modern_attendance_summary.modern_attendance_summary"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modern_attendance_summary.object', {
#             'object': obj
#         })
