# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class tracking_attachment_on_approval(models.Model):
#     _name = 'tracking_attachment_on_approval.tracking_attachment_on_approval'
#     _description = 'tracking_attachment_on_approval.tracking_attachment_on_approval'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
