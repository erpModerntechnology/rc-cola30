# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import fields, models, _
from odoo.exceptions import AccessDenied
from ast import literal_eval
import logging
_log = logging.getLogger(__name__)


class EmployeeAttendanceLocationWizard(models.TransientModel):
    _name = 'employee.attendance.location.wizard'
    _description = 'employee attendance location wizard'

    name = fields.Char(default="Employee Check In/Out Location")
    hr_attendance_ids = fields.Many2many('hr.attendance', string='Employee Attendances')
    active_cluster = fields.Boolean(string='Active Location Cluster', default=False)

    def _get_map_wizard(self, hr_attendance_ids, target=False, active_cluster=False):
        user_groups = self.env['ir.config_parameter'].sudo().get_param('employee_attendance_geolocations.attendance_geolocation_access_group')
        if user_groups:
            user_groups = literal_eval(user_groups)
            user_access = self.env['res.groups'].sudo().search([('id', 'in', user_groups), ('users.id', '=', self.env.user.id)], limit=1)
            if not user_access:
                raise AccessDenied()

        vals = {
            'hr_attendance_ids': [(6, 0, hr_attendance_ids)],
            'active_cluster': active_cluster
        }
        record = self.sudo().create(vals)
        action = self.env.ref('employee_attendance_geolocations.odoo_map_wizard_form_action').read()[0]
        action['res_id'] = record.id
        if target:
            action['target'] = target
        return action

    def action_hr_all_employee_attendance(self):
        today = fields.date.today()
        attendance_ids = self.env['hr.attendance'].sudo().search([
            ('check_in', '>=', today),
            ('geolocation_tracking', '=', True)
        ], order='id desc').ids
        return self._get_map_wizard(attendance_ids, active_cluster=True)
