# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MeetingNotification(models.Model):
    _inherit = ['']

# class meeting_telegram_notification(models.Model):
#     _name = 'meeting_telegram_notification.meeting_telegram_notification'
#     _description = 'meeting_telegram_notification.meeting_telegram_notification'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
