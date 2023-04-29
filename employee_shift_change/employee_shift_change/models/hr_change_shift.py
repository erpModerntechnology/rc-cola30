from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class HrChangeShift(models.Model):
    _name = 'hr.change.shift'
    _description = 'HrChangeShift'
    _rec_name = 'reference'

    reference = fields.Char(string='Reference', default=lambda self: _('Draft'), required=True, readonly=True,
                            copy=False)
    employee_id = fields.Many2one('hr.employee', required=True,default=lambda self:self.env.user.employee_id,readonly=True)
    employee_calendar_id = fields.Many2one('resource.calendar',default=lambda self:self.env.user.employee_id.resource_calendar_id,string="Employee Shift",readonly=True)
    manager_id = fields.Many2one('res.users',string="Manager")
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 default=lambda self: self.env.company)
    resource_calendar_id = fields.Many2one('resource.calendar', domain="['|','&', ('company_id', '=', False), ('company_id', '=', company_id),('id','!=',employee_calendar_id)]",required=True)
    request_date = fields.Date(default=fields.datetime.today())
    description = fields.Text()
    end_shift_date = fields.Date(
        string='End Shift Date',
        required=False)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('validate', 'Validated'),
        ('approve', 'Approved'),
        ('reject','Rejected'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    is_manager = fields.Boolean('Is Manager', compute='_compute_is_manager')
    can_confirm = fields.Boolean('Can Confirm', compute='_compute_can_confirm')
    can_validate = fields.Boolean('Can Validate', compute='_compute_can_validate')
    def _check_end_date(self):


            emp_shift_obj = self.env['hr.change.shift'].search([])

            for record in emp_shift_obj:


                if record.end_shift_date == fields.Datetime.today().date():
                    swap_id = record.employee_calendar_id
                    record.employee_calendar_id = record.resource_calendar_id
                    record.resource_calendar_id = swap_id
                    record.action_approved()
                    record.resource_calendar_id = record.employee_calendar_id
                    record.employee_calendar_id = swap_id


    @api.model
    def create(self, vals):
        if vals.get('reference', _('Draft')) == _('Draft'):  # get next sequence
            vals['reference'] = self.env['ir.sequence'].next_by_code('hr.change.shift') or _('New')
        res = super(HrChangeShift, self).create(vals)
        return res

    # @api.model
    # def default_get(self, default_fields):
    #     vals = super(HrChangeShift, self).default_get(default_fields)
    #     vals['manager_id'] = self.employee_id.parent_id.user_id.id
    #     print(vals['employee_id'])
    #     return vals

    def unlink(self):
        for record in self:
            if record.state == "approve":
                raise ValidationError(_("Can not delete request {} as it is approved".format(record.reference)))
            if record.state == "reject":
                raise ValidationError(_("Can not delete request {} as it is rejected".format(record.reference)))
        return super(HrChangeShift, self).unlink()

    @api.onchange('employee_id')
    def _on_change_employee(self):
        for record in self:
            if record.employee_id.parent_id:
                record.manager_id = record.employee_id.parent_id.user_id

    def _compute_is_manager(self):
            users = [r for r in self.env['res.users'].search([]) if r.has_group('hr.group_hr_manager')]
            if self.env.user in users:
                self.is_manager = True
            else:
                self.is_manager = False

    def _compute_can_confirm(self):
        user = self.env.user
        for record in self:
            if record.create_uid == user:
                record.can_confirm = True
            else:
                record.can_confirm = False

    def _compute_can_validate(self):
        user = self.env.user
        for record in self:
            if record.manager_id == user:
                record.can_validate = True
            else:
                record.can_validate = False

    def action_confirm(self):
        for record in self:
            user = record.manager_id
            record.send_manager_message(record,user)

            return record.write({'state': 'confirm'})

    def action_validate(self):
        for record in self:
            users = [r for r in self.env['res.users'].search([]) if r.has_group('hr.group_hr_manager')]
            for user in users:
                record.send_hr_message(record, user)

            return record.write({'state': 'validate'})

    def action_approved(self):
        for record in self:
            flag = 'Yes'
            employee_id = record.employee_id
            print(employee_id)
            print(employee_id.resource_calendar_id)
            print(employee_id.name)
            user_id = employee_id.user_id
            resource_calendar_id = record.resource_calendar_id
            if user_id:
                record.send_employee_message(record, user_id, flag)
            print(employee_id.resource_calendar_id)
            employee_id.write({'resource_calendar_id': resource_calendar_id.id})
            print(employee_id.resource_calendar_id)
            for contract in employee_id.contract_ids.filtered(lambda l:l.state in ['open','draft']):
                contract.write({'resource_calendar_id': resource_calendar_id.id})

            return record.write({'state': 'approve'})


    def action_reject(self):
        for record in self:
            flag = 'No'
            employee_id = record.employee_id
            user_id = employee_id.user_id
            if user_id:
                record.send_employee_message(record, user_id, flag)

            return record.write({'state': 'reject'})

    def send_manager_message(self, record, user, model_name='hr.change.shift'):
            notifications = [(0, 0, {
                'res_partner_id': user.partner_id.id,
                'notification_type': 'inbox',
                'is_read': False,
                'notification_status': 'ready',
            })]
            message = self.env['mail.message'].create({
                'subject': _(str(record.reference) + ' needs your attention.'),
                'model': model_name,
                'res_id': record.id,
                'message_type': 'notification',
                'body': 'Request for change work shift {doc} for employee {employee}'.format(
                    doc=record.reference, employee=record.employee_id.name),
                'subtype_id': self.env.ref('mail.mt_note').id,
                'notification_ids': notifications,
            })


    def send_hr_message(self, record, user, model_name='hr.change.shift'):
            notifications = [(0, 0, {
                'res_partner_id': user.partner_id.id,
                'notification_type': 'inbox',
                'is_read': False,
                'notification_status': 'ready',
            })]
            message = self.env['mail.message'].create({
                'subject': _(str(record.reference) + ' needs your attention.'),
                'model': model_name,
                'res_id': record.id,
                'message_type': 'notification',
                'body': 'Request for change work shift {doc} for employee {employee}'.format(
                    doc=record.reference, employee=record.employee_id.name),
                'subtype_id': self.env.ref('mail.mt_note').id,
                'notification_ids': notifications,
            })

    def send_employee_message(self, record, user,flag, model_name='hr.change.shift'):
        notifications = [(0, 0, {
            'res_partner_id': user.partner_id.id,
            'notification_type': 'inbox',
            'is_read': False,
            'notification_status': 'ready',
        })]
        message = self.env['mail.message'].create({
            'subject': _(str(record.reference) + ' needs your attention.'),
            'model': model_name,
            'res_id': record.id,
            'message_type': 'notification',
            'body': 'Please be notified that your request {doc} for changing your working shift that you requested at {req_date} has been approved by HR Manager.'.format(
                doc=record.reference,
                req_date=record.request_date) if flag == 'Yes' else 'Please be notified that your request {doc} for changing your working shift that you requested at {req_date} has been rejected by HR Manager.'.format(
                doc=record.reference, req_date=record.request_date),
            'subtype_id': self.env.ref('mail.mt_note').id,
            'notification_ids': notifications,
        })
