# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime,timedelta

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    renew = fields.Boolean(default=False)
    renew_status = fields.Selection([('approve', 'Approve'), ('refuse', 'Refuse')])

    def send_notification_to_checkin(self):
        # get current weekday
        weekday = str(datetime.now().weekday())
        self = self.env['hr.employee'].search([])
        start_date = datetime.now().replace(hour=3, minute=0,second=0)
        now = datetime.now()
        for employee in self:

            attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('check_in','>',start_date)],limit=1)
            if not attendance:
                calendar_id = employee.contract_id.resource_calendar_id.attendance_ids.filtered(lambda r: r.dayofweek == weekday)
                if calendar_id:
                    hour_from = calendar_id[0].hour_from
                    t1 = timedelta(hours=hour_from)
                    current_time = timedelta(hours=now.hour,minutes=now.minute,seconds=now.second)
                    if (current_time - t1).total_seconds() / 60  >= 15 and employee.user_id.partner_id:
                        employee.send_remind_notification()

    def send_remind_notification(self):
        self.ensure_one()
        notification_ids = []
        odoobot = self.env.ref('base.partner_root')
        notification_ids.append((0, 0, {
            'res_partner_id': self.user_id.partner_id.id,
            'notification_type': 'inbox'}))
        self.message_post(body="Attention you forgot to checkin in he system", message_type='notification',author_id=odoobot.id, notification_ids=notification_ids,partner_ids=[self.user_id.partner_id.id],)

    ##################################################################
    def send_activity_to_renew_contract(self,days_before):
        all_employee = self.env['hr.employee'].search([])

        for employee in all_employee:
            if employee.renew == False and employee.contract_id.date_end and (employee.contract_id.date_end - fields.date.today()).days < days_before:
                employee.send_activity()
                employee.renew = True
                employee.renew_status = False

    def send_activity(self):
        user_id = self.parent_id.user_id.id
        now = fields.datetime.now()
        date_deadline = now.date()
        activ_list = []
        if user_id and user_id != 'None':
            activity_id = self.sudo().activity_schedule(
                'mail.mail_activity_data_todo', date_deadline,
                note=('Contract Renewal'),
                user_id=user_id,
                res_id=self.id,

                summary=("PLZ renew contract for employee %s") % self.name
            )
            activ_list.append(activity_id.id)
            print(activ_list)
        [(4, 0, rec) for rec in activ_list]

    def activity_done(self):
        activity_ids = self.env['mail.activity'].sudo().search([('res_id', '=', self.id)])
        if activity_ids:
            for act in activity_ids:
                act.action_done()

    def renew_approve(self):
        self.activity_done()
        self.renew = False
        self.renew_status = 'approve'
        self.contract_id.send_activity_to_hr_manager()
        self.contract_id.renew = True
        self.contract_id.renew_status = False

    def renew_refuse(self):
        self.activity_done()
        self.renew = False
        self.renew_status = 'refuse'



