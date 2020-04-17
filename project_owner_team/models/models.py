# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class project_owner_team(models.Model):
#     _name = 'project_owner_team.project_owner_team'
#     _description = 'project_owner_team.project_owner_team'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
