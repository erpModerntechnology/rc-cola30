from odoo import models, fields


class commType(models.Model):
    _name = "employee.comm.type"
    _description = "Employee comm Type"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")


class comm(models.Model):
    _name = "employee.comm"
    _description = "Employee comm"

    name = fields.Char(string="Name")
    employee_id = fields.Many2one("hr.employee", string="Employee")
    date = fields.Date(string="Date")
    ttype = fields.Many2one('employee.comm.type', string=" نوع الكوميشن")
    amount = fields.Float(string="Amount")
    description = fields.Text(string="Description")
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.employee_id.company_id)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id')
