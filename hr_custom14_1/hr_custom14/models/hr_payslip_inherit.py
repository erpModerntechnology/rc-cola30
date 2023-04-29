# -*- coding: utf-8 -*-
from odoo import models, fields, api
import calendar


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    employee_policy_id = fields.Many2one('policy.group', string='Policy Group')

