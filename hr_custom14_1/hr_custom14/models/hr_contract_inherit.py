# -*- coding: utf-8 -*-
from odoo import models, fields,api
from lxml import etree



class HrContract(models.Model):
    _inherit = "hr.contract"

    renew = fields.Boolean(default=False)
    renew_status = fields.Selection([('approve','Approve'), ('refuse','Refuse')])

    def renew_approve(self):
        self.renew_status = 'approve'
        self.renew = False
        self.activity_done

    def renew_refuse(self):
        self.renew_status = 'refuse'
        self.renew = False
        self.activity_done

    def send_activity_to_hr_manager(self):
        user_id = self.hr_responsible_id.id
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

        [(4, 0, rec) for rec in activ_list]

    def activity_done(self):
        activity_ids = self.env['mail.activity'].sudo().search([('res_id', '=', self.id)])
        if activity_ids:
            for act in activity_ids:
                act.action_done()
