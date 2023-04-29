# -*- coding: utf-8 -*-
{
    'name': "Modern-tech Attendance Report",

    'summary': """
        Print Attendance Report for Employees""",

    'description': """
        This app helps you to print the attendances(Present and Absent Days) in PDF, based on Employees Calendar Resources.
    """,

    'author': "Ahmed Khalil",

    'category': 'Employees',

    'depends': ['base', 'hr_attendance'],
    'license': 'AGPL-3',

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/report_views.xml',
    ],
    "application": True,
    "installable": True,
}
