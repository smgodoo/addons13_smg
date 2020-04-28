# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'

    current_user = fields.Many2one('res.users', compute="_compute_current_user")
    current_user_id = fields.Integer(compute="_compute_current_user")
    project_user_id = fields.Integer(compute="_compute_project_user")

    def _compute_current_user(self):
        return self.env.user

    def _compute_project_user(self):
        user = self.env['res.users'].search([('id', '=', self.env.user.id)], limit=1)
        for record in self:
            record.current_user_id = user.id
            record.project_user_id = record.user_id.id
