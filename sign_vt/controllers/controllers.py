# -*- coding: utf-8 -*-
# from odoo import http


# class SignVt(http.Controller):
#     @http.route('/sign_vt/sign_vt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sign_vt/sign_vt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sign_vt.listing', {
#             'root': '/sign_vt/sign_vt',
#             'objects': http.request.env['sign_vt.sign_vt'].search([]),
#         })

#     @http.route('/sign_vt/sign_vt/objects/<model("sign_vt.sign_vt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sign_vt.object', {
#             'object': obj
#         })
