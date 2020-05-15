# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'
    company_ceo = fields.Many2one('res.users', string='Company CEO')


class Employee(models.Model):
    _inherit = 'hr.employee'
    hod = fields.Many2one('res.users', string='Head of department')


class ApprovalBudget(models.Model):
    _name = 'approval.budget'

    name = fields.Char()
    budget_min = fields.Integer()
    budget_max = fields.Integer()
    approver = fields.Selection([
        ('manager', 'Manager'),
        ('head_department', 'Head Department'),
        ('ceo', 'CEO')
    ])
    request_id = fields.Many2one(
        comodel_name="approval.category",
        string="Approval type request",
        ondelete="cascade",
        readonly=True,
    )


class ApprovalType(models.Model):
    _inherit = 'approval.category'

    budget_lines = fields.One2many(
        comodel_name="approval.budget",
        inverse_name="request_id", )
    is_hod_approver = fields.Boolean(stirng="Head Of Department",
                                     help="Automatically add the CEO as approver on the request.")
    is_ceo_approver = fields.Boolean(stirng="CEO",
                                     help="Automatically add the CEO as approver on the request.")


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    @api.onchange('category_id', 'request_owner_id')
    def _onchange_category_id(self):
        current_users = self.approver_ids.mapped('user_id')
        new_users = self.category_id.user_ids
        employee = self.env['hr.employee'].search([('user_id', '=', self.request_owner_id.id)], limit=1)
        if self.category_id.is_manager_approver:
            if employee.parent_id.user_id:
                new_users |= employee.parent_id.user_id
        if self.category_id.is_hod_approver:
            if employee.hod:
                new_users |= employee.hod
        if self.category_id.is_ceo_approver:
            company = self.env['res.company'].search([('id', '=', employee.company_id.id)], limit=1)
            if company.company_ceo:
                new_users |= company.company_ceo
        print(new_users)
        for user in new_users - current_users:
            self.approver_ids += self.env['approval.approver'].new({
                'user_id': user.id,
                'request_id': self.id,
                'status': 'new'})
