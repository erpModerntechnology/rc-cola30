{
    'name': 'Modern Tech Employee Late Check-in',
    'version': '14.0.1.0.0',
    'summary': """This module Allows Employee Late check-in deduction/penalty""",
    'description': """This module Allows Employee Late check-in deduction/penalty""",
    'author': "Ahmed Khalil",
    'company': 'Modern Technology',

    'maintainer': 'Modern  Technology Solutions',
    'category': 'Human Resources',
    'depends': ['hr_attendance', 'hr_payroll', 'hr_contract'],
    'data': [
        'views/res_config_settings.xml',
        'views/hr_attendance_view.xml',
        'views/late_check_in_view.xml',
        'views/hr_employee.xml',
        'security/ir.model.access.csv',
        'data/cron.xml',
        # 'data/salary_rule.xml',
    ],

    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
