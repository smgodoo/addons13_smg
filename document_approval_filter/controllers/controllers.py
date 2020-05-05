# -*- coding: utf-8 -*-
# from odoo import http


# class DocumentApprovalFilter(http.Controller):
#     @http.route('/document_approval_filter/document_approval_filter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/document_approval_filter/document_approval_filter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('document_approval_filter.listing', {
#             'root': '/document_approval_filter/document_approval_filter',
#             'objects': http.request.env['document_approval_filter.document_approval_filter'].search([]),
#         })

#     @http.route('/document_approval_filter/document_approval_filter/objects/<model("document_approval_filter.document_approval_filter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('document_approval_filter.object', {
#             'object': obj
#         })
