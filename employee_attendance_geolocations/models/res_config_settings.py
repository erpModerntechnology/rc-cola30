# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import models, fields, api, _
from ast import literal_eval

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_required_location = fields.Boolean(string='Required Employee Location', config_parameter='employee_attendance_geolocations.is_required_location')
    attendance_geolocation_access_group = fields.Many2many('res.groups', string='Allowed Group')
    allow_address = fields.Boolean(string='Allow Address On Map Maprker', config_parameter='employee_attendance_geolocations.allow_address')
    allow_distance = fields.Boolean(string='Allow Check In/Out Distance', config_parameter='employee_attendance_geolocations.allow_distance')

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('employee_attendance_geolocations.attendance_geolocation_access_group', self.attendance_geolocation_access_group.ids)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        attendance_geolocation_access_group = self.env['ir.config_parameter'].sudo().get_param('employee_attendance_geolocations.attendance_geolocation_access_group')
        if attendance_geolocation_access_group:
            res.update(attendance_geolocation_access_group=[(6, 0, literal_eval(attendance_geolocation_access_group))])
        return res
