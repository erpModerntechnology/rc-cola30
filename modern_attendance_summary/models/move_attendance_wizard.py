from odoo import fields, models, api
from datetime import date, timedelta
import pandas as pd
import datetime

class ModernMoveAttendance(models.TransientModel):
    _name = 'modern.move.attendance.wizard'



    date_from = fields.Date(
        string='From',
        required=False)
    date_to = fields.Date(
        string='To',
        required=False)
    emp_id = fields.Many2one('hr.employee', 'HR Employee')


    def move_attendance(self):
        domain=[]
        attendance_obj = self.env['hr.attendance']
        leabve_obj = self.env['hr.leave']
        if self.emp_id:
            all_employee = self.env['hr.employee'].search([('id','=',self.emp_id.id)])
        else:
            all_employee = self.env['hr.employee'].search([])
        start_date = self.date_from

        end_date = self.date_to
        delta = timedelta(days=1)
        daterange = pd.date_range(start_date, end_date)
        for single_date in daterange:
            # dd1 =single_date.strftime("%Y-%m-%d").date()
            dd =single_date.strftime("%Y-%m-%d")
            # print(single_date.strftime("%Y-%m-%d"))
            # print(single_date)
            # print('---------------------------')
            for emp in all_employee:
                attendance_obj = attendance_obj.search([('checkin_date','=',dd),('employee_id','=',emp.id)])

                if attendance_obj:
                    for att in attendance_obj:
                        if_att_exist = self.env['modern.hr.attendance'].search([('emp_id','=', emp.id),('check_in','=', att.checkin_date)])
                        if not if_att_exist:
                            s = self.env['modern.hr.attendance'].create({
                                    'emp_id': emp.id,
                                    'check_in': att.checkin_date,
                                    'check_out': att.checkout_date,
                                    # 'work_from':attendance_obj.work_from,
                                    # 'work_to':attendance_obj.work_to,
                                    'holiday': False,
                                    'apsent': False,

                                })

                else:
                        leabve_obj = leabve_obj.search([('employee_id','=',emp.id)])
                        print(leabve_obj)
                        if leabve_obj:
                            for leave in leabve_obj:

                                dd1 = datetime.datetime.strptime(dd,"%Y-%m-%d").date()
                                # print(type(dd1))
                                if leave.request_date_from <= dd1 <= leave.request_date_to:

                                    if_att_exist = self.env['modern.hr.attendance'].search(
                                        [('emp_id', '=', emp.id), ('date', '=', dd1)])
                                    if not if_att_exist:
                                        s = self.env['modern.hr.attendance'].create({
                                            'emp_id': emp.id,
                                            'date': dd1,
                                            # 'check_out': attendance_obj.checkout_date,
                                            # 'work_from':attendance_obj.work_from,
                                            # 'work_to':attendance_obj.work_to,
                                            'holiday': True,
                                            'apsent': False,

                                        })
                                else:
                                    if_att_exist = self.env['modern.hr.attendance'].search(
                                        [('emp_id', '=', emp.id), ('date', '=', dd1)])
                                    if not if_att_exist:
                                        s = self.env['modern.hr.attendance'].create({
                                            'emp_id': emp.id,
                                            'date': dd1,
                                            # 'check_out': attendance_obj.checkout_date,
                                            # 'work_from': attendance_obj.work_from,
                                            # 'work_to': attendance_obj.work_to,
                                            'holiday': False,
                                            'apsent': True,

                                        })


                        else:
                            if_att_exist = self.env['modern.hr.attendance'].search(
                                [('emp_id', '=', emp.id), ('date', '=', dd)])
                            if not if_att_exist:

                                s = self.env['modern.hr.attendance'].create({
                                    'emp_id':emp.id,
                                    'date':dd ,
                                    # 'check_out': attendance_obj.checkout_date,
                                    # 'work_from':attendance_obj.work_from,
                                    # 'work_to':attendance_obj.work_to,
                                    'holiday': False,
                                    'apsent': True,

                            })


