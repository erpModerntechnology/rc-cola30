# -*- coding: utf-8 -*-
{
    'name': "HR Custom 14",
    'summary': """HR Policy""",
    'category': 'Human Resources',

    'description': """""",
    'version': '0.1',
    'depends': ['hr','hr_contract', 'hr_attendance'],

    'data': [
        'data/data.xml',
        'views/hr_contract_inherit_view.xml',
        'views/hr_employee_inherit_view.xml'
    ],

    'installable': True,
    'auto_install': False,
}
