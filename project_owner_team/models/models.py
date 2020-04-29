# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'

    can_edit_record = fields.Boolean(default=False, compute="_compute_project_user")

    def _compute_current_user(self):
        return self.env.user

    def _compute_project_user(self):
        for record in self:
            if record.user_id.id == self.env.user.id:
                record.can_edit_record = True
            print(record.can_edit_record)
