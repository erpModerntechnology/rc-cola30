# -*- coding: utf-8 -*-
{
    'name': "Change Employee Shift",
    'summary': """
    Employee Request Change his Shift
    
    """,
    'author': "modernTech",
    'website': "",
    'category': 'Human Resources',
    'version': '0.1',

    'depends': ['hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/hr_change_shift.xml'
    ]
}

