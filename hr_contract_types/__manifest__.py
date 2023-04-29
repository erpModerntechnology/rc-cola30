# -*- coding: utf-8 -*-

{
    'name': ' Modern Tchnology Odoo14 Employee Contracts Types',
    'version': '14.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'summary': """
        Contract type in contracts
    """,
    'description': """Odoo14 Employee Contracts Types,Odoo14 Employee, Employee Contracts, Odoo 14""",
    'author': 'Ahmed Khalil',
    'company': 'Modern Techhnology',
    'maintainer': 'Modern Techhnology Solutions',

    'depends': ['hr', 'hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/contract_view.xml',
        'data/hr_contract_type_data.xml',
    ],
    'installable': True,

    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}