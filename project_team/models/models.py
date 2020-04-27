# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTeam(models.Model):
    _name = 'project.team_vt'

    name = fields.Char()
    active = fields.Boolean(default=True)
    members = fields.Many2many('res.partner')


class ProjectProject(models.Model):
    _inherit = 'project.project'

    members_vt = fields.Many2many('res.partner', string='Members_VT')
    team_id_vt = fields.Many2one('project.team_vt', string="Project Team")

    @api.onchange('team_id_vt')
    def onchange_team_id_vt(self):
        self.members_vt = False
        if self.team_id_vt:
            self.members_vt = [(6, 0, [member.id for member in self.team_id_vt.members])]
