# -*- coding: utf-8 -*-

from odoo import models, fields, api,_,SUPERUSER_ID


class TrainingStage(models.Model):
    _name = "training.stage"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(string="اسم المرحله")

    success_stage = fields.Boolean(
        string='Success stage',
        required=False ,group_expand='_read_group_stage_ids')
    description = fields.Char(
        string='Description', 
        required=False)
class Training(models.Model):
    _name = "modern.hr.training"
    _inherit = ['mail.thread', ]
    _description = "Training"

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """ Override read_group to always display all states. """
        group_by_field = 'state'
        group_by_selection = self._fields[group_by_field].selection
        if groupby and groupby[0] == group_by_field:
            # Default result structure
            read_group_all_states = [{
                '__context': {'group_by': groupby[1:]},
                group_by_field + '_count': 0,
                '__domain': domain + [(group_by_field, '=', selection_key)],
                group_by_field: selection_key, }
                for selection_key, selection_value in group_by_selection]
            # Get standard results
            read_group_res = super(Training, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                             orderby=orderby, lazy=lazy)
            # Update standard results with default results
            result = []
            for selection_key, selection_value in group_by_selection:
                res = list(filter(lambda x: x[group_by_field] == selection_key, read_group_res))
                if not res:
                    res = list(filter(lambda x: x[group_by_field] == selection_key, read_group_all_states))
                result.append(res[0])
            return result
        else:
            return super(Repairs, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby,
                                                   lazy=lazy)

    name = fields.Char(string="عنوان الدورة")
    employee_ids = fields.Many2many('hr.employee', string="الموظفون")
    emp_id = fields.Many2one('hr.employee', 'المدرب')

    from_date = fields.Date(string="بداية الدورة التدريبية")
    to_date = fields.Date(string=" نهاية الدورة التدريبيه")

    train_side = fields.Char(string="جهة التدريب")
    train_type = fields.Selection([('train_in', 'تدريب داخلي'),
                               ('train_out', 'تدريب خارجي'),],
                              string=" نوع التدريب")
    stage_id = fields.Many2one('training.stage', 'Stage', )
    state = fields.Selection([
        ('new', 'دورة جاهزه جديدة'),
        ('start', 'انطلاق الدورة'),
        ('complete', 'الدوره مكتملة'),
        ('cancel', 'الدورة ملغية'),], 'Status')

    description = fields.Text(string="التفاصيل")




    @api.onchange('state')
    def onchange_method(self):
        if self.state == "complete":
            print(self.state)
            all_course = self.search([('name','=',self.name)])
            print(all_course)
            notification_ids_manager = []

            all_user = self.env['res.users'].search([])
            for course in all_course:




                names = ''
                for em in course.employee_ids:
                    if em.leave_manager_id:
                        notification_ids_manager.append((0, 0, {
                            'res_partner_id': em.leave_manager_id.partner_id.id,
                            'notification_type': 'inbox'}))
                        em.with_user(self.env.ref('base.user_admin')).message_post(
                            body="لقد تم الانتهاء من التدريب للموظف  : " + em.name, message_type='notification',
                            subtype_xmlid='mail.mt_comment',
                            notification_ids=notification_ids_manager)
                        names += "   " + em.name + " , "
                print(names)


                notification_ids = []

                for user in all_user:
                    if user.has_group("modern_hr_training.employee_notification_group"):
                        print(user)

                        notification_ids.append((0, 0, {
                                'res_partner_id': user.partner_id.id,
                                'notification_type': 'inbox'}))

                        print(notification_ids)



                course.with_user(self.env.ref('base.user_admin')).message_post(body="لقد تم الانتهاء من التدريب لهؤلاء الموظفين  : " + names, message_type='notification',
                                  subtype_xmlid='mail.mt_comment',
                                  notification_ids=notification_ids)






            # self.message_post(
            #     subject=_('Your taxes have been updated !'),
            #     author_id=self.env.user.id,
            #     body="ahmed",
            #     message_type='notification',
            #     subtype_xmlid='mail.mt_comment',
            #     partner_ids=user.partner_id,
            # )
            # self.env['mail.message'].create({
            #     'email_from': self.env.user.partner_id.email,  # add the sender email
            #     'author_id': self.env.user.partner_id.id,  # add the creator id
            #     'model': 'mail.channel',  # model should be mail.channel
            #
            #     'subtype_id': self.env.ref('mail.mt_comment').id,
            #     'body': "لقد تم الانتهاء من التدريب لهؤلاء الموظفين  : " + names,  # here add the message body
            #     'channel_ids': [(4, self.env.ref('mail.channel_all_employees').id)],
            #     # This is the channel where you want to send the message and all the users of this channel will receive message
            #     'res_id': self.env.ref('mail.channel_all_employees').id,  # here add the channel you created.
            # })
            #
            #
            #
            #
