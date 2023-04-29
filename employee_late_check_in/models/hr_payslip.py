# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Ijaz Ahammed (odoo@cybrosys.com)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import models, api, fields,_
from odoo.tools.float_utils import float_round
from datetime import datetime, timedelta
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
import math
from collections import namedtuple
DummyAttendance = namedtuple('DummyAttendance', 'hour_from, hour_to, dayofweek, day_period, week_type')

from pytz import timezone, UTC


class HrLeave(models.Model):
    _inherit = "hr.leave"

    @api.depends('request_date_from_period', 'request_hour_from', 'request_hour_to', 'request_date_from',
                 'request_date_to',
                 'request_unit_half', 'request_unit_hours', 'request_unit_custom', 'employee_id')
    def _compute_date_from_to(self):
        print("ahewesad")
        for holiday in self:
            print(holiday)
            if holiday.request_date_from and holiday.request_date_to and holiday.request_date_from > holiday.request_date_to:
                holiday.request_date_to = holiday.request_date_from
            if not holiday.request_date_from:
                holiday.date_from = False
            elif not holiday.request_unit_half and not holiday.request_unit_hours and not holiday.request_date_to:
                holiday.date_to = False
            else:
                if holiday.request_unit_half or holiday.request_unit_hours:
                    holiday.request_date_to = holiday.request_date_from
                resource_calendar_id = holiday.employee_id.resource_calendar_id or self.env.company.resource_calendar_id
                domain = [('calendar_id', '=', resource_calendar_id.id), ('display_type', '=', False)]
                attendances = self.env['resource.calendar.attendance'].read_group(domain, ['ids:array_agg(id)',
                                                                                           'hour_from:min(hour_from)',
                                                                                           'hour_to:max(hour_to)',
                                                                                           'week_type', 'dayofweek',
                                                                                           'day_period'],
                                                                                  ['week_type', 'dayofweek',
                                                                                   'day_period'], lazy=False)

                # Must be sorted by dayofweek ASC and day_period DESC
                attendances = sorted([DummyAttendance(group['hour_from'], group['hour_to'], group['dayofweek'],
                                                      group['day_period'], group['week_type']) for group in
                                      attendances], key=lambda att: (att.dayofweek, att.day_period != 'morning'))

                default_value = DummyAttendance(0, 0, 0, 'morning', False)

                if resource_calendar_id.two_weeks_calendar:
                    # find week type of start_date
                    start_week_type = int(math.floor((holiday.request_date_from.toordinal() - 1) / 7) % 2)
                    attendance_actual_week = [att for att in attendances if
                                              att.week_type is False or int(att.week_type) == start_week_type]
                    attendance_actual_next_week = [att for att in attendances if
                                                   att.week_type is False or int(att.week_type) != start_week_type]
                    # First, add days of actual week coming after date_from
                    attendance_filtred = [att for att in attendance_actual_week if
                                          int(att.dayofweek) >= holiday.request_date_from.weekday()]
                    # Second, add days of the other type of week
                    attendance_filtred += list(attendance_actual_next_week)
                    # Third, add days of actual week (to consider days that we have remove first because they coming before date_from)
                    attendance_filtred += list(attendance_actual_week)

                    end_week_type = int(math.floor((holiday.request_date_to.toordinal() - 1) / 7) % 2)
                    attendance_actual_week = [att for att in attendances if
                                              att.week_type is False or int(att.week_type) == end_week_type]
                    attendance_actual_next_week = [att for att in attendances if
                                                   att.week_type is False or int(att.week_type) != end_week_type]
                    attendance_filtred_reversed = list(reversed([att for att in attendance_actual_week if
                                                                 int(att.dayofweek) <= holiday.request_date_to.weekday()]))
                    attendance_filtred_reversed += list(reversed(attendance_actual_next_week))
                    attendance_filtred_reversed += list(reversed(attendance_actual_week))

                    # find first attendance coming after first_day
                    attendance_from = attendance_filtred[0]
                    # find last attendance coming before last_day
                    attendance_to = attendance_filtred_reversed[0]
                else:
                    # find first attendance coming after first_day
                    attendance_from = next(
                        (att for att in attendances if int(att.dayofweek) >= holiday.request_date_from.weekday()),
                        attendances[0] if attendances else default_value)
                    # find last attendance coming before last_day
                    attendance_to = next((att for att in reversed(attendances) if
                                          int(att.dayofweek) <= holiday.request_date_to.weekday()),
                                         attendances[-1] if attendances else default_value)

                compensated_request_date_from = holiday.request_date_from
                compensated_request_date_to = holiday.request_date_to

                if holiday.request_unit_half:
                    if holiday.request_date_from_period == 'am':
                        hour_from = float_to_time(attendance_from.hour_from)
                        hour_to = float_to_time(attendance_from.hour_to)
                    else:
                        hour_from = float_to_time(attendance_to.hour_from)
                        hour_to = float_to_time(attendance_to.hour_to)
                elif holiday.request_unit_hours:
                    hour_from = float_to_time(float(holiday.request_hour_from))
                    hour_to = float_to_time(float(holiday.request_hour_to))
                    print("ahme kjasdlkjasasdas",hour_to,hour_from)
                elif holiday.request_unit_custom:
                    hour_from = holiday.date_from.time()
                    hour_to = holiday.date_to.time()
                    print("ahme kjasdlkjasasdas")

                    compensated_request_date_from = holiday._adjust_date_based_on_tz(holiday.request_date_from,
                                                                                     hour_from)
                    compensated_request_date_to = holiday._adjust_date_based_on_tz(holiday.request_date_to, hour_to)
                else:
                    hour_from = float_to_time(attendance_from.hour_from)
                    hour_to = float_to_time(attendance_to.hour_to)

                print("holiday.date_from, holiday.date_to")
                print(holiday.date_from, holiday.date_to)
                holiday.date_from = holiday.date_from +timedelta(hours=2)
                holiday.date_to = holiday.date_to +timedelta(hours=3)
                print(holiday.date_from, holiday.date_to)
                holiday.date_from = timezone(holiday.tz).localize(
                    datetime.combine(compensated_request_date_from, hour_from)).astimezone(UTC).replace(tzinfo=None)
                holiday.date_to = timezone(holiday.tz).localize(
                    datetime.combine(compensated_request_date_to, hour_to)).astimezone(UTC).replace(tzinfo=None)
                print(holiday.date_from,holiday.date_to)
    @api.depends('number_of_hours_display')
    @api.onchange('request_hour_from')
    def _compute_number_of_hours_text(self):
        print("ajew")
        # YTI Note: All this because a readonly field takes all the width on edit mode...
        for leave in self:
            leave.number_of_hours_text = '%s%g %s%s' % (
                '' if leave.request_unit_half or leave.request_unit_hours else '(',
                float_round(leave.number_of_hours_display, precision_digits=2),
                _('Hours'),
                '' if leave.request_unit_half or leave.request_unit_hours else ')')
            print(leave.number_of_hours_text)
            print(leave.number_of_hours_display)

        @api.depends('number_of_days')
        @api.onchange('request_hour_from')
        def _compute_number_of_hours_display(self):
            print("aslkdhalksdhla")

            for holiday in self:
                print("aslkdhalksdhla")
                calendar = holiday._get_calendar()
                if holiday.date_from and holiday.date_to:
                    # Take attendances into account, in case the leave validated
                    # Otherwise, this will result into number_of_hours = 0
                    # and number_of_hours_display = 0 or (#day * calendar.hours_per_day),
                    # which could be wrong if the employee doesn't work the same number
                    # hours each day
                    if holiday.state == 'validate':
                        start_dt = holiday.date_from
                        end_dt = holiday.date_to
                        # if not start_dt.tzinfo:
                        #     start_dt = start_dt.replace(tzinfo=UTC)
                        # if not end_dt.tzinfo:
                        #     end_dt = end_dt.replace(tzinfo=UTC)
                        resource = holiday.employee_id.resource_id
                        intervals = calendar._attendance_intervals_batch(start_dt, end_dt, resource)[resource.id] \
                                    - calendar._leave_intervals_batch(start_dt, end_dt, None)[
                                        False]  # Substract Global Leaves
                        number_of_hours = sum((stop - start).total_seconds() / 3600 for start, stop, dummy in intervals)
                    else:
                        number_of_hours = \
                        holiday._get_number_of_days(holiday.date_from, holiday.date_to, holiday.employee_id.id)['hours']
                    holiday.number_of_hours_display = number_of_hours or (
                                holiday.number_of_days * (calendar.hours_per_day or HOURS_PER_DAY))
                else:
                    holiday.number_of_hours_display = 0


class PayslipLateCheckIn(models.Model):
    _inherit = 'hr.payslip'

    late_check_in_ids = fields.Many2many('late.check_in')

    @api.model
    def get_inputs(self, contracts, date_from, date_to):
        """
        function used for writing late check-in record in payslip
        input tree.

        """
        res = super(PayslipLateCheckIn, self).get_inputs(contracts, date_to, date_from)
        late_check_in_type = self.env.ref('employee_late_check_in.late_check_in')
        contract = self.contract_id
        late_check_in_id = self.env['late.check_in'].search([('employee_id', '=', self.employee_id.id),
                                                             ('date', '<=', self.date_to),
                                                             ('date', '>=', self.date_from),
                                                             ('state', '=', 'approved'),
                                                             ])
        amount = late_check_in_id.mapped('amount')
        cash_amount = sum(amount)
        if late_check_in_id:
            self.late_check_in_ids = late_check_in_id
            input_data = {
                'name': late_check_in_type.name,
                'code': late_check_in_type.code,
                'amount': cash_amount,
                'contract_id': contract.id,
            }
            res.append(input_data)
        return res

    def action_payslip_done(self):
        """
        function used for marking deducted Late check-in
        request.

        """
        for recd in self.late_check_in_ids:
            recd.state = 'deducted'
        return super(PayslipLateCheckIn, self).action_payslip_done()
