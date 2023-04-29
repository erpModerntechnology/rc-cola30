# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ContractType(models.Model):
    _name = 'hr.contract.type'
    _description = 'Contract Type'
    _order = 'sequence, id'

    name = fields.Char(string='Contract Type', required=True, help="Name")
    sequence = fields.Integer(help="Gives the sequence when displaying a list of Contract.", default=10)


class ContractInherit(models.Model):
    _inherit = 'hr.contract'

    type_id = fields.Many2one('hr.contract.type', string="Employee Category",
                              required=True, help="Employee category",
                              default=lambda self: self.env['hr.contract.type'].search([], limit=1))

    @api.onchange('state')
    def onchange_method(self):
        notification_ids_manager = []
        if self.state == "close":
            for rec in self:
                print(rec.employee_id.name)
                notification_ids_manager.append((0, 0, {
                    'res_partner_id': rec.employee_id.parent_id.user_id.partner_id.id,
                    'notification_type': 'inbox'}))

                w = rec.employee_id.with_user(self.env.ref('base.user_admin')).message_post(
                    body="لقد تم نتهاء العقد   : " + rec.employee_id.name, message_type='notification',
                    subtype_xmlid='mail.mt_comment',
                    notification_ids=notification_ids_manager)
                print(w)




