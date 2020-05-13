# -*- coding: utf-8 -*-
# from odoo import http


# class ApprovalBudgetLevel(http.Controller):
#     @http.route('/approval_budget_level/approval_budget_level/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/approval_budget_level/approval_budget_level/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('approval_budget_level.listing', {
#             'root': '/approval_budget_level/approval_budget_level',
#             'objects': http.request.env['approval_budget_level.approval_budget_level'].search([]),
#         })

#     @http.route('/approval_budget_level/approval_budget_level/objects/<model("approval_budget_level.approval_budget_level"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('approval_budget_level.object', {
#             'object': obj
#         })
