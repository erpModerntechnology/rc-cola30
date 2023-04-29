from odoo import api, fields, models
from datetime import datetime
class TrainingNotification(models.Model):
    _name = 'training.notification'
    _description = 'training.notification'
    def get_ended_training(self):
        print(datetime.today().date())
        employee =  self.env['employee.training'].search([('to_date','<',datetime.today().date())])
        names = ''
        for em in employee:
            names+= "   "+em.employee_id.name + " , "
        self.action_send_notification(names)
    def action_send_notification(self,names):
        self.env['mail.message'].create({
            'email_from': self.env.user.partner_id.email,  # add the sender email
            'author_id': self.env.user.partner_id.id,  # add the creator id
            'model': 'mail.channel',  # model should be mail.channel

            'subtype_id': self.env.ref('mail.mt_comment').id,
            'body': "لقد تم الانتهاء من التدريب لهؤلاء الموظفين  : "+names,  # here add the message body
             'channel_ids': [(4, self.env.ref('mail.channel_all_employees').id)],  # This is the channel where you want to send the message and all the users of this channel will receive message
            'res_id': self.env.ref('mail.channel_all_employees').id,  # here add the channel you created.
        })


