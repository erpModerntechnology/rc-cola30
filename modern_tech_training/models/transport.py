from odoo import models, fields


class TransType(models.Model):
    _name = "employee.trans.type"
    _description = "Employee trans Type"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")


class trans(models.Model):
    _name = "employee.trans"
    _description = "Employee trans"

    name = fields.Char(string="Name")
    employee_id = fields.Many2one("hr.employee", string="Employee")
    date = fields.Date(string="Date")
    ttype = fields.Many2one('employee.trans.type', string="نوع النقل")
    amount = fields.Float(string="Amount")
    description = fields.Text(string="Description")
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.employee_id.company_id)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id')
