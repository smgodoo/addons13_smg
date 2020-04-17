# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectOwnerTeam(http.Controller):
#     @http.route('/project_owner_team/project_owner_team/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_owner_team/project_owner_team/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_owner_team.listing', {
#             'root': '/project_owner_team/project_owner_team',
#             'objects': http.request.env['project_owner_team.project_owner_team'].search([]),
#         })

#     @http.route('/project_owner_team/project_owner_team/objects/<model("project_owner_team.project_owner_team"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_owner_team.object', {
#             'object': obj
#         })
