# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Notification',
    'version': '1.0',
    'summary': 'Create Notification to Mangers on attendance and time off ',
    'description': "",
    'website': '',
    'depends': ['account', 'purchase', 'sale', 'stock','hr_attendance','mail','hr_holidays'],
    'sequence': -100,
    'data': [
        'views/res_config.xml'
    ],
    'license': 'LGPL-3'

}
