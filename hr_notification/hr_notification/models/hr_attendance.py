from odoo import models, fields, api, exceptions, _
from odoo.tools import format_datetime
from datetime import datetime
from datetime import datetime, timedelta, date


class HrAttendance(models.Model):
    _name = "hr.attendance"
    _inherit = ['hr.attendance','mail.activity.mixin','mail.thread']
    delay_duration = fields.Float(string="Max Limit", config_parameter='attendance.delay_duration')

    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        """ Verifies the validity of the attendance record compared to the others from the same employee.
            For the same employee we must have :
                * maximum 1 "open" attendance record (without check_out)
                * no overlapping time slices with previous employee records
        """
        for attendance in self:


            # notification_ids = []
            # for user in attendance_Managers:
            #     notification_ids.append((0, 0, {
            #         'res_partner_id': user.partner_id.id,
            #         'notification_type': 'inbox'}))
            # self.env['mail.message'].message_post(body='This receipt has been validated!', message_type='notification',
            #                                       author_id='self.env.user.partner_id.id',
            #                                      notification_ids=notification_ids)

            # we take the latest attendance before our check_in time and check it doesn't overlap with ours
            last_attendance_before_check_in = self.env['hr.attendance'].search([
                ('employee_id', '=', attendance.employee_id.id),
                ('check_in', '<=', attendance.check_in),
                ('id', '!=', attendance.id),
            ], order='check_in desc', limit=1)
            if last_attendance_before_check_in and last_attendance_before_check_in.check_out and last_attendance_before_check_in.check_out > attendance.check_in:
                raise exceptions.ValidationError(
                    _("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                        'empl_name': attendance.employee_id.name,
                        'datetime': format_datetime(self.env, attendance.check_in, dt_format=False),
                    })

            if not attendance.check_out:
                # if our attendance is "open" (no check_out), we verify there is no other "open" attendance
                no_check_out_attendances = self.env['hr.attendance'].search([
                    ('employee_id', '=', attendance.employee_id.id),
                    ('check_out', '=', False),
                    ('id', '!=', attendance.id),
                ], order='check_in desc', limit=1)
                if no_check_out_attendances:
                    raise exceptions.ValidationError(
                        _("Cannot create new attendance record for %(empl_name)s, the employee hasn't checked out since %(datetime)s") % {
                            'empl_name': attendance.employee_id.name,
                            'datetime': format_datetime(self.env, no_check_out_attendances.check_in, dt_format=False),
                        })
            else:
                # we verify that the latest attendance with check_in time before our check_out time
                # is the same as the one before our check_in time computed before, otherwise it overlaps
                last_attendance_before_check_out = self.env['hr.attendance'].search([
                    ('employee_id', '=', attendance.employee_id.id),
                    ('check_in', '<', attendance.check_out),
                    ('id', '!=', attendance.id),
                ], order='check_in desc', limit=1)
                if last_attendance_before_check_out and last_attendance_before_check_in != last_attendance_before_check_out:
                    raise exceptions.ValidationError(
                        _("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                            'empl_name': attendance.employee_id.name,
                            'datetime': format_datetime(self.env, last_attendance_before_check_out.check_in,
                                                        dt_format=False),
                        })
            type = "check out"
            check = attendance.check_out
            if not attendance.check_out:
                type = "check in"
                check = attendance.check_in
            if type=='check in':
                self.check_in_late(attendance,check,type)
            else:
                self.check_out_early(attendance,check,type)


    def check_in_late(self,attendance,check,type):

        attendance_Manager_groups = self.env['res.groups'].sudo().search(
            [('name', '=', 'Administrator'), ('category_id.name', '=', 'Attendances')])
        attendance_Managers = self.env['res.users'].sudo().search(
            [('groups_id.name', '=', 'Administrator'), ('groups_id.category_id.name', '=', 'Attendances')])
        note = _(
            '%(user)s Made %(leave_type)s at %(check_)s',
            leave_type=type,
            user=self.env.user.name,
            check_=check
        )
        self.delay_duration = self.env['ir.config_parameter'].sudo().get_param('attendance.delay_duration')
        print(self.delay_duration)
        if attendance.employee_id.contract_id:
            work_schedule = attendance.sudo().employee_id.contract_id.resource_calendar_id
            for schedule in work_schedule.sudo().attendance_ids:
                today = datetime.now()
                todayofweek=today.weekday()
                if schedule.dayofweek==str(todayofweek):
                    work_from = schedule.hour_from
                    result = '{0:02.0f}:{1:02.0f}'.format(*divmod(work_from * 60, 60))
                    user_tz = self.env.user.tz
                    dt = attendance.check_in
                    dt = attendance.check_in + timedelta(hours=2)
                    str_time = dt.strftime("%H:%M")
                    check_in_date = datetime.strptime(str_time, "%H:%M").time()
                    start_date = datetime.strptime(result, "%H:%M").time()
                    t1 = timedelta(hours=check_in_date.hour, minutes=check_in_date.minute)
                    t2 = timedelta(hours=start_date.hour, minutes=self.delay_duration)
                    # t2 = timedelta(hours=start_date.hour, minutes=start_date.minute)
                    if check_in_date > start_date:
                        final = t1 - t2
                        model_id = self.env['ir.model']._get(self._name).id
                        for manger in attendance_Managers:
                            if manger.id != self.env.user.id:
                                create_vals = {
                                    'res_name': self.env.user.name,
                                    'activity_type_id': 1,
                                    'summary': "",
                                    'automated': True,
                                    'note': note,
                                    'date_deadline': fields.Date.context_today(self),
                                    'res_model_id': model_id,
                                    'res_id': self.id,
                                    'user_id': manger.id
                                }
                                self.env['mail.activity'].sudo().create(create_vals)

                            # attendance.activity_schedule(
                            #     'hr_holidays.mail_act_leave_approval',
                            #     note=note,
                            #     user_id=manger.partner_id.id or self.env.user.id)

                            # notification_ids = [(0, 0,
                            #                      {
                            #                          'res_partner_id': manger.partner_id.id,
                            #                          'notification_type': 'email'
                            #                      }
                            #                      )]
                            #
                            # # self.env['mail.thread'].sudo().message_notify(
                            # #     notification_ids= notification_ids,
                            # #     message_type="notification",
                            # #     subject="%s %s"%(self.env.user.name,type),
                            # #     body="%s %s at %s" % (self.env.user.name,type,check),
                            # #     author_id=self.env.user.partner_id and self.env.user.partner_id.id,
                            # #     partner_ids=[manger.partner_id.id],
                            # #     record_name="Attendance",
                            # #     # email_layout_xmlid='mail.mail_notification_light',
                            # # )
                            # self.env['mail.message'].create({
                            #     "subtype_id": 2,
                            #     'email_from':"odoobot@example.com",
                            #     'message_type': "notification",
                            #     'body': " %s at %s" % (type,check),
                            #     'subject': "%s %s"%(self.env.user.name,type),
                            #     "partner_ids":[(4,manger.partner_id.id)],
                            #     'model': self._name,
                            #     'res_id': self.id,
                            #     'record_name':"%s %s"%(self.env.user.name,type),
                            #     'notification_ids': notification_ids,
                            #     'author_id':  self.env.user.partner_id.id
                            # })
                            # ch_obj = self.env['mail.channel']
                            # ch_name = manger.name + ', ' + self.env.user.name
                            # ch = ch_obj.sudo().search([('name', 'ilike', str(ch_name))])
                            # if not ch:
                            #     ch = ch_obj.sudo().search([('name', 'ilike', str(self.env.user.name + ', ' + manger.name))])
                            # if not ch:
                            #     channel_odoo_bot_users = '%s, %s' % (manger.name, self.env.user.name)
                            #     ch = ch_obj.create({
                            #         'name': channel_odoo_bot_users,
                            #         'email_send': False,
                            #         'channel_type': 'chat',
                            #         'public': 'private',
                            #         'channel_partner_ids': [(4, manger.partner_id.id), (4, self.env.user.partner_id.id)]
                            #     })
                            # ch.message_post(
                            #     notification_ids=notification_ids,
                            #     attachment_ids=[],
                            #     body="%s %s at %s" % (self.env.user.name,type,check),
                            #     subject="%s %s"%(self.env.user.name,type),
                            #     message_type='comment', partner_ids=[],
                            #     record_name=self.env.user.name)

    def check_out_early(self, attendance, check,type):
        attendance_Manager_groups = self.env['res.groups'].sudo().search(
            [('name', '=', 'Administrator'), ('category_id.name', '=', 'Attendances')])
        attendance_Managers = self.env['res.users'].sudo().search(
            [('groups_id.name', '=', 'Administrator'), ('groups_id.category_id.name', '=', 'Attendances')])
        note = _(
            '%(user)s Made %(leave_type)s at %(check_)s',
            leave_type=type,
            user=self.env.user.name,
            check_=check
        )
        model_id = self.env['ir.model']._get(self._name).id
        for manger in attendance_Managers:
            if manger.id != self.env.user.id:
                create_vals = {
                    'res_name': self.env.user.name,
                    'activity_type_id': 1,
                    'summary': "",
                    'automated': True,
                    'note': note,
                    'date_deadline': fields.Date.context_today(self),
                    'res_model_id': model_id,
                    'res_id': self.id,
                    'user_id': manger.id
                }
                self.env['mail.activity'].sudo().create(create_vals)