# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class AttendanceInherit(models.Model):

    _inherit = 'hr.attendance'

    work_from = fields.Float(string="Work From",  required=False,store=True)
    work_to = fields.Float(string="Work To",  required=False,store=True)
    branch_id = fields.Many2one('res.branch', 'Branch',related='employee_id.branch_id' ,store=True)
    flagg = fields.Boolean("flag"  ,default=False)

    @api.depends('work_from')
    def _compute_work_from(self):
        for rec in self:
            work_from = rec.work_from
            work_to = rec.to
            if not rec.flagg :
                attend = rec.employee_id.resource_calendar_id.attendance_ids
                for i in attend :
                    rec.work_from=i.hour_from
                rec.flagg = True
            else:
                rec.work_from = work_from
                rec.work_to=work_to

    @api.depends('work_to')
    def _compute_work_to(self):
        to1 = 0
        for rec in self:
            attend = rec.employee_id.resource_calendar_id.attendance_ids
            for i in attend:
                rec.work_to = i.hour_to

