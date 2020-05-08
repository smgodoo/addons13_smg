# -*- coding: utf-8 -*-
# from odoo import http


# class TicketFollowerTeam(http.Controller):
#     @http.route('/ticket_follower_team/ticket_follower_team/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ticket_follower_team/ticket_follower_team/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ticket_follower_team.listing', {
#             'root': '/ticket_follower_team/ticket_follower_team',
#             'objects': http.request.env['ticket_follower_team.ticket_follower_team'].search([]),
#         })

#     @http.route('/ticket_follower_team/ticket_follower_team/objects/<model("ticket_follower_team.ticket_follower_team"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ticket_follower_team.object', {
#             'object': obj
#         })
