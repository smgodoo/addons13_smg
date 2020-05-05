# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ApprovalRequest(models.Model):
    _inherit = ['approval.request']

    department_id = fields.Many2one('hr.department', string='Department', track_visibility='onchange')
