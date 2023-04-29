# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import fields, _
from odoo.http import request, route
from odoo.addons.hr_attendance.controllers.main import HrAttendance
import logging
_log = logging.getLogger(__name__)


class HrAttendanceGelocation(HrAttendance):

    def get_redirect_url_for_location(self, employee, allow_distance):
        if allow_distance and employee.check_out and not employee.same_location:
            return 'origin=%s,%s&destination=%s,%s'%(employee.check_in_latitude, employee.check_in_longitude, employee.check_out_latitude, employee.check_out_longitude)
        return False

    def _get_employee_attendance_domain(self, filter={}):
        domain = [('geolocation_tracking', '=', True)]
        date_from = filter.get('date_from')
        date_to = filter.get('date_to')
        today = fields.Date.today()
        message_from = False
        message_to = False

        if filter.get('search_item'):
            field_name = 'employee_id.%s'%filter.get('search_field', 'name')
            domain.append((field_name, 'ilike', filter['search_item']))
        if date_from:
            domain.append(('check_in', '>=', date_from))
            message_from = date_from
            if not date_to:
                message_to = today
                domain.append(('check_in', '<=', today))
        if date_to:
            message_to = date_to
            domain.append(('check_in', '<=', date_to))
            if not date_from:
                message_from = date_to
                domain.append(('check_in', '>=', date_to))
        if not date_to and not date_from:
            domain.append(('check_in', '>=', today))
        return (domain, message_from, message_to)

    @route(['/hr_attendance_geolocation'], auth='user', type='json', csrf=False)
    def hr_attendance_geolocation(self, hr_attendance_ids=[], filter={}, **kw):
        AttendanceSudo = request.env['hr.attendance'].sudo()

        ConfigParameter = request.env['ir.config_parameter'].sudo()
        active_address = ConfigParameter.get_param('employee_attendance_geolocations.allow_address')
        allow_distance = ConfigParameter.get_param('employee_attendance_geolocations.allow_distance')
        emp_attendances = []
        header_info = _('Report #Today')

        google_api_key = request.env['ir.config_parameter'].sudo().get_param('base_geolocalize.google_map_api_key')
        if google_api_key:
            google_js = '//maps.google.com/maps/api/js?key=%s'%google_api_key
        else:
            google_js = '//maps.google.com/maps/api/js'

        if filter:
            domain, message_from, message_to = self._get_employee_attendance_domain(filter)
            attendance_ids = AttendanceSudo.search(domain)
            if message_from and message_to:
                header_info = _('Report #From %s #To %s') %(message_from, message_to)
        else:
            attendance_ids = AttendanceSudo.browse(hr_attendance_ids)

        for attendance in attendance_ids:
            if attendance.geolocation_tracking:
                values = []
                redirect_url = self.get_redirect_url_for_location(attendance, allow_distance)
                if attendance.check_in and attendance.check_in_latitude and attendance.check_in_longitude:
                    values.append({
                        'name': attendance.employee_id.name,
                        'date': attendance.check_in.date(),
                        'time': attendance.check_in.time(),
                        'lat': attendance.check_in_latitude,
                        'long': attendance.check_in_longitude,
                        'type': _('Check In Information'),
                        'device_type': attendance.check_in_device,
                        'redirect_url': redirect_url
                    })
                if attendance.check_out and attendance.check_out_latitude and attendance.check_out_longitude:
                    check_out_location = {
                        'name': attendance.employee_id.name,
                        'date': attendance.check_out.date(),
                        'time': attendance.check_out.time(),
                        'lat': attendance.check_out_latitude,
                        'long': attendance.check_out_longitude,
                        'type': _('Check Out Information'),
                        'device_type': attendance.check_out_device
                    }
                    if attendance.same_location and len(values) > 0:
                        values[0]['same_location'] = True
                        values[0]['same_location'] = True
                        values[0]['check_out_location'] = check_out_location
                    else:
                        check_out_location.update(redirect_url=redirect_url)
                        values.append(check_out_location)
                emp_attendances.extend(values)
        return {
            'active_address': active_address,
            'emp_attendances': emp_attendances,
            'header_info': header_info,
            'google_js': google_js
        }
