from odoo import models, fields, api, exceptions, _
from odoo.tools import format_datetime

class ConfSetting(models.TransientModel):
   _inherit = "res.config.settings"
   delay_duration = fields.Float(string="Delay Duration", store=True)

   def set_values(self):
      res = super(ConfSetting, self).set_values()
      self.env['ir.config_parameter'].sudo().set_param('attendance.delay_duration', self.delay_duration)
      # self.env['ir.config_parameter'].sudo().set_param('discount.discount_limit', self.discount_limit)
      limit = self.env['ir.config_parameter'].get_param('attendance.delay_duration')
      print(limit)
      return res

   @api.model
   def get_values(self):
      res = super(ConfSetting, self).get_values()
      ICPSudo = self.env['ir.config_parameter'].sudo()
      res.update(
         delay_duration=ICPSudo.get_param('attendance.delay_duration'),
         # discount_limit=ICPSudo.get_param('discount.discount_limit'),
      )
      return res
