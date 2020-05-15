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
    is_hod_approver = fields.Boolean(string="Head Of Department",
                                     help="Automatically add Head Of Department as approver on the request.")
    is_ceo_approver = fields.Boolean(string="CEO",
                                     help="Automatically add CEO as approver on the request.")


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    request_status = fields.Selection([
        ('new', 'To Submit'),
        ('pending', 'Submitted'),
        ('on_hold', ' On-Hold'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('cancel', 'Cancel')], default="new", compute="_compute_request_status", store=True, compute_sudo=True,
        group_expand='_read_group_request_status')
    user_status = fields.Selection([
        ('new', 'New'),
        ('pending', 'To Approve'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('on_hold', ' On-Hold'),
        ('cancel', 'Cancel')], compute="_compute_user_status")

    @api.depends('approver_ids.status')
    def _compute_user_status(self):
        for approval in self:
            approval.user_status = approval.approver_ids.filtered(
                lambda approver: approver.user_id == self.env.user).status

    @api.depends('approver_ids.status')
    def _compute_request_status(self):
        for request in self:
            status_lst = request.mapped('approver_ids.status')
            minimal_approver = request.approval_minimum if len(status_lst) >= request.approval_minimum else len(
                status_lst)
            if status_lst:
                if status_lst.count('cancel'):
                    status = 'cancel'
                elif status_lst.count('refused'):
                    status = 'refused'
                elif status_lst.count('new'):
                    status = 'new'
                elif status_lst.count('on_hold'):
                    status = 'on_hold'
                elif status_lst.count('approved') >= minimal_approver:
                    status = 'approved'
                else:
                    status = 'pending'
            else:
                status = 'new'
            request.request_status = status

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

    def action_on_hold(self, approver=None):
        if not isinstance(approver, models.BaseModel):
            approver = self.mapped('approver_ids').filtered(
                lambda approver: approver.user_id == self.env.user
            )
        approver.write({'status': 'on_hold'})
        self.sudo()._get_user_approval_activities(user=self.env.user).action_feedback()


class ApprovalApprover(models.Model):
    _inherit = 'approval.approver'

    status = fields.Selection([
        ('new', 'New'),
        ('pending', 'To Approve'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('on_hold', ' On-Hold'),
        ('cancel', 'Cancel')], string="Status", default="new", readonly=True)