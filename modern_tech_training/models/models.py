# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Training(models.Model):
    _name = "hr.training"
    _description = "Training"

    name = fields.Char(string="Name")
    from_date = fields.Date(string="From Date")
    course_subject = fields.Char(string="Course Subject")
    to_date = fields.Date(string="To Date")
    status = fields.Selection([('start', 'To Start'),
                               ('running', 'Running'),
                               ('hold', 'Hold'),
                               ('cancel', 'Cancel'),
                               ('Done', 'Done')], default='start',
                              string="Status")
    employee_ids = fields.One2many('employee.training','hr_training_id', string="Employee")
    description = fields.Text(string="Description")
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)



class EmployeeTraining(models.Model):
    _name = "employee.training"
    _description = "Employee Training"

    name = fields.Char(string=" Course Name")
    employee_id = fields.Many2one("hr.employee", string="Employee")
    hr_training_id = fields.Many2one("hr.training", string="Training Program")
    result = fields.Char(string='Result')
    from_date = fields.Date(string="From Date")
    course_subject = fields.Char(string="Course Subject", related='hr_training_id.course_subject')
    to_date = fields.Date(string="To Date")
    status = fields.Selection([('start', 'To Start'),
                               ('running', 'Running'),
                               ('hold', 'Hold'),
                               ('cancel', 'Cancel'),
                               ('Done', 'Done')], default='start',
                              string="Status")
    description = fields.Text(string="Description")
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)


class HREmployee(models.Model):
    _inherit = 'hr.employee'


    @api.model
    def fields_get(self, fields=None):
        hide = ['create_uid','create_date','activity_type_icon','activity_ids','user_partner_id','message_follower_ids','tz','leave_manager_id','sinid','write_date','write_uid','last_attendance_id','image_512','image_256','image_128','image_1024','message_channel_ids','departure_date','departure_reason','contract_warning','message_partner_ids','activity_exception_decoration','message_needaction','color','ssnid','last_check_in','last_check_out','attendance_ids','is_absent']

        res = super(HREmployee, self).fields_get()
        for field in hide:

            res[field]['searchable'] = False

        return res


    punish_ids = fields.One2many("employee.punish", "employee_id", string="العقويات")
    reward_ids = fields.One2many("employee.reward", "employee_id", string="العقويات")
    training_ids = fields.One2many("employee.training", "employee_id", string="Training")
    zmm_ids = fields.One2many("hr.zmm", "employee_id", string="Training")
    bonus_ids = fields.One2many("employee.bonus", "employee_id", string="البونص")
    trans_ids = fields.One2many("employee.trans", "employee_id", string="النقل")
    comm_ids = fields.One2many("employee.comm", "employee_id", string="الكوميشن")

    latee = fields.Float(string="التاخير",  required=False, )
    early_leave = fields.Float(string="الرحيل المبكر ",  required=False, )
    days_latee = fields.Float(string="ايام الغياب",  required=False, )
    pre_job = fields.Char(string="Previous Job ", required=False, )



class HrZmm(models.Model):
    _name = 'hr.zmm'
    name = fields.Char("الاسم")
    note = fields.Char("الملاحظات")
    date = fields.Date(string="تاريخ الاستلام", required=False, )
    amount = fields.Float(string=" القيمه",  required=False, )
    employee_id = fields.Many2one("hr.employee", string="Employee")
