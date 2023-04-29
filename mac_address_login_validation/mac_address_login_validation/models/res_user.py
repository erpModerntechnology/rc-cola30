
import logging
import subprocess
import sys
from odoo import models, fields, api, _

py_v = "python%s.%s" % (sys.version_info.major, sys.version_info.minor)

_logger = logging.getLogger(__name__)
try:
    from getmac import get_mac_address as gma
except ImportError:
    _logger.info('\n There was no such module named -getmac- installed')
    _logger.info('xxxxxxxxxxxxxxxx installing getmac xxxxxxxxxxxxxx')
    subprocess.check_call([py_v, "-m", "pip", "install", "--user", "getmac"])
    from getmac import get_mac_address as gma


class ResUsers(models.Model):
    _inherit = 'res.users'

    mac_address_ids = fields.One2many('mac.address', 'res_user_id',
                                      string='Allowed MAC IDs')
    enable_mac_address_login = fields.Boolean(default=False,help="Enable MAC Address Login.")
    current_mac_address = fields.Char(compute='_get_current_mac',)

    def _get_current_mac(self):
        for rec in self:
            rec.current_mac_address = gma()

    @api.onchange('enable_mac_address_login')
    def _onchange_enable_mac_address_login(self):
        for rec in self:
            if not rec.enable_mac_address_login:
                rec.mac_address_ids = False


class MacAddress(models.Model):
    _name = 'mac.address'
    _description = 'User MAC Address Registration'

    name = fields.Char(string="Description")
    mac_address = fields.Char(string="MAC Address")
    res_user_id = fields.Many2one('res.users')
