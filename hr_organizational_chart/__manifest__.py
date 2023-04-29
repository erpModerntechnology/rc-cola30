
{
    'name': ' Modern Techhnology HR Organizational Chart',
    'version': '14.0.1.0.0',
    'summary': 'HR Employees organizational chart',
    'description': 'HR Employees organizational chart',
    'author': 'Modern Techhnology',
    'company': 'Modern Techhnology Solutions',


    'depends': ['hr'],
    'data': [
        'views/show_employee_chart.xml',
        'views/assets.xml',
    ],
    'qweb': ['static/src/xml/chart_view.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}