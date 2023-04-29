from odoo import api, fields, models,_
class HrEmployeTraining(models.Model):
     _inherit = 'hr.employee'
     def _compute_success_course_count(self):

         for rec in self:

             all_training = self.env['modern.hr.training'].search([ ('employee_ids', 'in', rec.id),('stage_id.success_stage', '=', True)])

             rec.success_course_count =len(all_training)
     success_course_count = fields.Integer(
         string='Success course',
          compute='_compute_success_course_count')

     def action_to_open_success_training(self):
         domain = [
             ('employee_ids', 'in', self.id),
             ('stage_id.success_stage', '=', True),
         ]
         return {
             'name': _('الدورات المجتازه'),
             'domain': domain,
             'res_model': 'modern.hr.training',
             'type': 'ir.actions.act_window',
             'view_mode': 'tree,form',
             'limit': 80,
         }
 
