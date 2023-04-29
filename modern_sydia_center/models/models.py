# -*- coding: utf-8 -*-

from odoo import models, fields, api

class NewModule1(models.Model):
    _name = 'saydia.line'
    clock = fields.Float(
        string='الساعه',
        required=False)
    bp = fields.Char(
        string='Bp',
        required=False)
    pr = fields.Char(
        string='PR',
        required=False)
    spo2 = fields.Char(
        string='Spo2',
        required=False)
    tere = fields.Char(
        string='Tere',
        required=False)
    center_id = fields.Many2one(
        comodel_name='sydia.center',
        string='Center_id',
        required=False)

class saydiaTreatment(models.Model):
    _name = 'saydia.treatment'
    treatment_id = fields.Many2one(
        comodel_name='sydia.center',
        string='Center_id',
        required=False)
    clock = fields.Float(
        string='الساعه',
        required=False)
    treatment = fields.Char(
        string='Treatment ',
        required=False)



class modern_sydia_center(models.Model):
    _name = 'sydia.center'
    name = fields.Char("الاسم")
    age = fields.Char("العمر")
    gender = fields.Selection(
        [('M', 'Male'), ('F', 'Female')], 'الجنس', required=True)
    arrive_date = fields.Date(
        string='تاريخ الوصول للطوارئ',
        required=False)
    clock = fields.Float(
        string='الساعه',
        required=False)
    hsasiya = fields.Char(
        string='حساسيه دوائيه',
        required=False)
    chronic_diseases = fields.Selection(
        string='امراض مزمنه',
        selection=[('press','ضغط'),
                   ('suger', 'سكر'),
                   ('heart', 'قلب'),
                   ('etc', 'أخري'),
                   ],
        required=False, )

    state = fields.Char(
        string='حالة المريض بدخوله الطوائ',
        required=False)
    sick_state = fields.Selection(
        string='حاله المريض',
        selection=[('out', 'خروج'),
                   ('wait', 'انتظار'),
                   ('rkod', 'رقود'),
                   ],
        required=False, )
    saydia_line= fields.One2many(
        comodel_name='saydia.line',
        inverse_name='center_id',
        string='حاله المريض',
        required=False)
    saydia_treatment = fields.One2many(
            comodel_name='saydia.treatment',
            inverse_name='treatment_id',
            string='العلاجات',
            required=False)
    clock2 = fields.Float(
        string='الساعه',
        required=False)
    date2 = fields.Date(
        string='التاريخ',
        required=False)
    signature = fields.Binary("التوقيع")
    
    

