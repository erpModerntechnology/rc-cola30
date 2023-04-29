import logging
import math

from collections import defaultdict, namedtuple

from datetime import datetime, date, timedelta, time
from dateutil.rrule import rrule, DAILY
from pytz import timezone, UTC

from odoo import api, fields, models, SUPERUSER_ID, tools
from odoo.addons.base.models.res_partner import _tz_get
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_compare, format_date
from odoo.tools.float_utils import float_round
from odoo.tools.translate import _
from odoo.osv import expression
class HolidaysRequest(models.Model):
    _inherit = "hr.leave"

    @api.model_create_multi
    def create(self, vals_list):
        attendance_Manager_groups = self.env['res.groups'].sudo().search(
            [('name', '=', 'Administrator'), ('category_id.name', '=', 'Time Off')])
        attendance_Managers = self.env['res.users'].sudo().search(
            [('groups_id.name', '=', 'Administrator'), ('groups_id.category_id.name', '=', 'Time Off')])
        """ Override to avoid automatic logging of creation """
        if not self._context.get('leave_fast_create'):
            leave_types = self.env['hr.leave.type'].browse(
                [values.get('holiday_status_id') for values in vals_list if values.get('holiday_status_id')])
            mapped_validation_type = {leave_type.id: leave_type.leave_validation_type for leave_type in leave_types}
            for values in vals_list:

                employee_id = values.get('employee_id', False)
                leave_type_id = values.get('holiday_status_id')
                # Handle automatic department_id
                if not values.get('department_id'):
                    values.update({'department_id': self.env['hr.employee'].browse(employee_id).department_id.id})

                # Handle no_validation
                if mapped_validation_type[leave_type_id] == 'no_validation':
                    values.update({'state': 'confirm'})

                if 'state' not in values:
                    # To mimic the behavior of compute_state that was always triggered, as the field was readonly
                    values['state'] = 'confirm' if mapped_validation_type[leave_type_id] != 'no_validation' else 'draft'

                # Handle double validation
                if mapped_validation_type[leave_type_id] == 'both':
                    self._check_double_validation_rules(employee_id, values.get('state', False))

        holidays = super(HolidaysRequest, self.with_context(mail_create_nosubscribe=True)).create(vals_list)

        for holiday in holidays:
            if not self._context.get('leave_fast_create'):
                # Everything that is done here must be done using sudo because we might
                # have different create and write rights
                # eg : holidays_user can create a leave request with validation_type = 'manager' for someone else
                # but they can only write on it if they are leave_manager_id
                holiday_sudo = holiday.sudo()
                holiday_sudo.add_follower(employee_id)
                if holiday.validation_type == 'manager':
                    holiday_sudo.message_subscribe(partner_ids=holiday.employee_id.leave_manager_id.partner_id.ids)
                if holiday.validation_type == 'no_validation':
                    # Automatic validation should be done in sudo, because user might not have the rights to do it by himself
                    holiday_sudo.action_validate()
                    holiday_sudo.message_subscribe(partner_ids=[holiday._get_responsible_for_approval().partner_id.id])
                    holiday_sudo.message_post(body=_("The time off has been automatically approved"),
                                              subtype_xmlid="mail.mt_comment")  # Message from OdooBot (sudo)
                elif not self._context.get('import_file'):
                    holiday_sudo.activity_update()
        note = _(
            '%(user)s Made %(leave_type)s ',
            leave_type='Time Off',
            user=self.env.user.name,
            # check_=datetime.now().strftime()
        )
        model_id = self.env['ir.model']._get(self._name).id
        for manger in attendance_Managers:
            create_vals = {
                'res_name': self.env.user.name,
                'activity_type_id': 1,
                'summary': "",
                'automated': True,
                'note': note,
                'date_deadline': fields.Date.context_today(self),
                'res_model_id': model_id,
                'res_id': holidays.id,
                'user_id': manger.id
            }
            self.env['mail.activity'].sudo().create(create_vals)
            # notification_ids = [(0, 0,
            #                      {
            #                          'res_partner_id': manger.partner_id.id,
            #                          'notification_type': 'email'
            #                      }
            #                      )]
            # self.env['mail.message'].sudo().create({
            #     "subtype_id": 2,
            #     'email_from': "odoobot@example.com",
            #     'message_type': "notification",
            #     'body': "%s Time Off from %s to %s" % (
            #     self.env.user.name, values.get('date_from'), values.get('date_to')),
            #     'subject': "%s Time Off" % (self.env.user.name),
            #     "partner_ids": [(4, manger.partner_id.id)],
            #     'model': self._name,
            #     'res_id': self.id,
            #     'record_name': "%s Time Off" % (self.env.user.name),
            #     'notification_ids': notification_ids,
            #     'author_id': self.env.user.partner_id.id
            # })
        return holidays