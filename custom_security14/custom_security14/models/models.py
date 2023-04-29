# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class custom_security14(models.Model):
#     _name = 'custom_security14.custom_security14'
#     _description = 'custom_security14.custom_security14'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
