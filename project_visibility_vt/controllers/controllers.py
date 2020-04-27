# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectVisibilityVt(http.Controller):
#     @http.route('/project_visibility_vt/project_visibility_vt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_visibility_vt/project_visibility_vt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_visibility_vt.listing', {
#             'root': '/project_visibility_vt/project_visibility_vt',
#             'objects': http.request.env['project_visibility_vt.project_visibility_vt'].search([]),
#         })

#     @http.route('/project_visibility_vt/project_visibility_vt/objects/<model("project_visibility_vt.project_visibility_vt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_visibility_vt.object', {
#             'object': obj
#         })
