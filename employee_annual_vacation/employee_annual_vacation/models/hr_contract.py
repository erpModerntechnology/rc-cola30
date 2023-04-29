# -*- coding: utf-8 -*-
from odoo import fields, models,api,_
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class HrContractInherit(models.Model):
    _inherit = "hr.contract"


    allocation_flag = fields.Boolean()
    holiday_status_id = fields.Many2one(
        "hr.leave.type", string="Annual Time Off Type",domain=[('request_unit','=','day')])
    employee_annual_credit = fields.Float(
        string="Employee Annual Timeoff credit",copy=False)

    def create_leave_allocation(self):
        for contract in self:
            if not contract.allocation_flag:
                contract_start = contract.date_start
                contract_end = contract.date_end or contract.date_start.replace(month=12, day=31)
                if not contract.holiday_status_id:
                    raise ValidationError(_('Please specify the annual timeoff vacation for the employee before creating allocations!'))

                if not contract.employee_annual_credit:
                    raise ValidationError(_('Please specify the annual timeoff vacation credit for employee {} before creating allocations!'.format(contract.employee_id.name)))

                employee_year_credit = contract.employee_annual_credit
                years_duration = ((contract_end.year - contract_start.year) * 12 + contract_end.month - contract_start.month) + 1


                for i in range(0, years_duration):
                        allocation_vals = {
                            'name': 'Allocation for employee %s from %s  to %s of %s' % (
                                contract.employee_id.name, contract_start + relativedelta(months=i * 1), contract_end,
                                contract.holiday_status_id.name),
                            'employee_id': contract.employee_id.id,
                            'holiday_status_id': contract.holiday_status_id.id,
                            'date_from': contract_start + relativedelta(months=i * 1),
                            'date_to': contract_end,
                            'number_of_days': (employee_year_credit / 12),
                        }
                        allocation = self.env['hr.leave.allocation'].create(allocation_vals)
                        allocation.action_validate()

                contract.allocation_flag = True




