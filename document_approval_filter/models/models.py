# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ApprovalRequest(models.Model):
    _inherit = ['approval.request']

    sub_category_id = fields.Many2one('approval.category', string='Sub Category')
    department_id = fields.Many2one('hr.department', string='Department', track_visibility='onchange')

    @api.onchange('category_id')
    def onchange_category_id(self):
        self.sub_category_id = []
        return {'domain': {'sub_category_id': [('parent_id', 'in', [self.category_id.id])]}}


class ApprovalsCategory(models.Model):
    _inherit = 'approval.category'

    parent_id = fields.Many2one('approval.category')
