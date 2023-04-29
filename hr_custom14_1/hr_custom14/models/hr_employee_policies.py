# -*- coding: utf-8 -*-
from odoo import models,api, fields, _
from lxml import etree


class PolicyGroup(models.Model):
    _name = 'policy.group'
    _description = "Policy Group"

    name = fields.Char(string="Policy Group", required=1)

class InhEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(InhEmployee, self).fields_view_get(view_id=view_id,view_type=view_type,toolbar=toolbar,submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field,value in res['fields'].items():
                if field and (value['type'] == 'many2one' or value['type'] == 'many2many'):
                    for node in doc.xpath("//field[@name='%s']" % field):
                        node.attrib['can_create'] = 'false'
                        node.attrib['can_write'] = 'false'
            res['arch'] = etree.tostring(doc)
        return res
