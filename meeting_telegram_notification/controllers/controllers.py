# -*- coding: utf-8 -*-
# from odoo import http


# class MeetingTelegramNotification(http.Controller):
#     @http.route('/meeting_telegram_notification/meeting_telegram_notification/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/meeting_telegram_notification/meeting_telegram_notification/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('meeting_telegram_notification.listing', {
#             'root': '/meeting_telegram_notification/meeting_telegram_notification',
#             'objects': http.request.env['meeting_telegram_notification.meeting_telegram_notification'].search([]),
#         })

#     @http.route('/meeting_telegram_notification/meeting_telegram_notification/objects/<model("meeting_telegram_notification.meeting_telegram_notification"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('meeting_telegram_notification.object', {
#             'object': obj
#         })
