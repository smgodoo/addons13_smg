# -*- coding: utf-8 -*-
# from odoo import http


# class TrackingAttachmentOnApproval(http.Controller):
#     @http.route('/tracking_attachment_on_approval/tracking_attachment_on_approval/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tracking_attachment_on_approval/tracking_attachment_on_approval/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tracking_attachment_on_approval.listing', {
#             'root': '/tracking_attachment_on_approval/tracking_attachment_on_approval',
#             'objects': http.request.env['tracking_attachment_on_approval.tracking_attachment_on_approval'].search([]),
#         })

#     @http.route('/tracking_attachment_on_approval/tracking_attachment_on_approval/objects/<model("tracking_attachment_on_approval.tracking_attachment_on_approval"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tracking_attachment_on_approval.object', {
#             'object': obj
#         })
