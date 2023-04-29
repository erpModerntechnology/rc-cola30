
{
    'name': 'Biometric Device Integration',
    'version': '14.0.1.0.0',
    'summary': """Integrating Biometric Device (Model: ZKteco uFace 202) With HR Attendance (Face + Thumb)""",
    'description': """This module integrates Odoo with the biometric device(Model: ZKteco uFace 202),odoo13,odd,hr,attendance""",
    'category': 'Generic Modules/Human Resources',
    'author': 'Cybrosys Techno Solutions, Mostafa Shokiel',
    'company': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['base_setup', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/zk_machine_view.xml',
        'views/zk_machine_attendance_view.xml',
        'data/download_data.xml'

    ],
    'images': ['static/description/banner.gif'],
    'license': 'AGPL-3',
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
