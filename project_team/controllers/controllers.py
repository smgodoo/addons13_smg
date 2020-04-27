# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectTeam(http.Controller):
#     @http.route('/project_team/project_team/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_team/project_team/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_team.listing', {
#             'root': '/project_team/project_team',
#             'objects': http.request.env['project_team.project_team'].search([]),
#         })

#     @http.route('/project_team/project_team/objects/<model("project_team.project_team"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_team.object', {
#             'object': obj
#         })
