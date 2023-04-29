# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
_log = logging.getLogger(__name__)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    geolocation_tracking = fields.Boolean(string='Geolocation Tracking', default=False)
    check_in_latitude = fields.Float(string='Check In Lat')
    check_in_longitude = fields.Float(string='Check In Long')
    check_out_latitude = fields.Float(string='Check Out Lat')
    check_out_longitude = fields.Float(string='Check Out Long')
    check_in_device = fields.Selection([('mobile', 'Mobile'), ('system', 'System')])
    check_out_device = fields.Selection([('mobile', 'Mobile'), ('system', 'System')])
    same_location = fields.Boolean(string='Check In/Out Same Location', default=False)

    def is_required_location(self):
        ConfigParameter = self.env['ir.config_parameter'].sudo()
        is_required_location = ConfigParameter.get_param('employee_attendance_geolocations.is_required_location') or False
        return is_required_location

    def set_employee_check_in_out_location(self, lat=False, long=False, device_type='system'):
        self.ensure_one()
        if lat and long:
            self.geolocation_tracking = True
            if not self.check_out:
                self.check_in_latitude = lat
                self.check_in_longitude = long
                self.check_in_device = device_type
            else:
                self.check_out_latitude = lat
                self.check_out_longitude = long
                self.check_out_device = device_type
                if self.check_in_latitude and self.check_in_longitude:
                    if round(self.check_in_latitude, 3) == round(lat, 3) and round(self.check_in_longitude, 3) == round(long, 3):
                        self.same_location = True
        return True

    def action_employee_check_in_out_location(self, check_in=True):
        self.ensure_one()
        if self.geolocation_tracking:
            wizard = self.env['employee.attendance.location.wizard'].sudo()
            return wizard._get_map_wizard([self.id], 'new')
        raise ValidationError(_('Geolocation Tracking is not active for this entry'))
