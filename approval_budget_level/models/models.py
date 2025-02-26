# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'
    company_ceo = fields.Many2one('res.users', string='Company CEO')


class ApprovalTypeBudgetLine(models.Model):
    _name = 'approval.budget.line'

    name = fields.Char(required=True)
    sequence_number = fields.Integer()
    max_budget = fields.Float()
    approval_level = fields.Selection(selection=[
        ('manager_level', 'Manager'),
        ('manager_and_hod', 'Manager and Head of department'),
        ('ceo_level', 'CEO')
    ], default='manager_level')
    budget_type_id = fields.Many2one('approval.category',
                                     string='Approval Type Reference',
                                     required=True, ondelete='cascade',
                                     index=True,
                                     copy=False)
    _sql_constraints = [
        ('sequence_number', 'unique (sequence_number)', 'The sequence_number already Exists!'),
    ]


class Employee(models.Model):
    _inherit = 'hr.employee'
    hod = fields.Many2one('hr.employee', string='Head of department')
    supervisor = fields.Many2one('hr.employee', string='Supervisor')
    senior = fields.Many2one('hr.employee', string='Senior')


class ApprovalSubject(models.Model):
    _name = 'approval.subject'
    _description = "Apply title for approval.request"
    name = fields.Char(required=True)
    department_id = fields.Many2one('hr.department')


class ApprovalRequestTitle(models.Model):
    _inherit = 'approval.request'
    name = fields.Char(required=False)
    approval_subject = fields.Many2one('approval.subject', required=True)

    @api.onchange('department_id')
    def onchange_department_id(self):
        self.approval_subject = []
        return {'domain': {'approval_subject': ['|', ('department_id', 'in', [self.department_id.id]),
                                                ('department_id', '=', False)]}}

    @api.model
    def create(self, vals):
        if vals.get('approval_subject'):
            subject = self.env['approval.subject'].search([('id', '=', vals.get('approval_subject'))], limit=1)
            vals['name'] = subject.name
        return super(ApprovalRequestTitle, self).create(vals)


class EmployeePublic(models.Model):
    _inherit = 'hr.employee.public'
    hod = fields.Many2one('hr.employee.public', string='Head of department')
    supervisor = fields.Many2one('hr.employee.public', string='Supervisor')
    senior = fields.Many2one('hr.employee.public', string='Senior')


class ApprovalType(models.Model):
    _inherit = 'approval.category'
    department_s = fields.Many2one(comodel_name='approval.department', inverse_name="request_id")
    is_hod_approver = fields.Boolean(string="Head Of Department",
                                     help="Automatically add Head Of Department as approver on the request.")
    is_ceo_approver = fields.Boolean(string="CEO",
                                     help="Automatically add CEO as approver on the request.")
    is_supervisor = fields.Boolean(string='Supervisor', help="Automatically add Supervisor as approver")
    is_senior = fields.Boolean(string='Senior',
                               help="Automatically add Senior as approver")
    is_manual_approval = fields.Boolean(string="Manual ?")

    has_follower_after_approved = fields.Boolean(default=False)
    followers = fields.Many2many('res.partner')
    approval_budget_line = fields.One2many('approval.budget.line', 'budget_type_id', string='Budget Lines',
                                           copy=True,
                                           auto_join=True)

    def create_request(self):
        self.ensure_one()
        employee = self.env['hr.employee.public'].search([('user_id', '=', self.env.user.id)], limit=1)
        return {
            "type": "ir.actions.act_window",
            "res_model": "approval.request",
            "views": [[False, "form"]],
            "context": {
                'form_view_initial_mode': 'edit',
                'hide_name': True,
                'default_name': self.name,
                'default_department_id': employee.department_id.id,
                'default_category_id': self.id,
                'default_request_owner_id': self.env.user.id,
                'default_request_status': 'new'
            },
        }


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
    show_final_approval = fields.Boolean(default=False, compute='_compute_final_approval_button')
    final_approve = fields.Boolean(default=False, tracking=True)
    minimal_approval = fields.Integer(default=1)

    def _compute_final_approval_button(self):
        company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
        employee_obj = self.env['hr.employee']
        show_final_approval = ['pending', 'on_hold']
        for record in self:
            r_status = False
            employee = employee_obj.search([('user_id', '=', record.request_owner_id.id)])
            if employee:
                if record.category_id.is_ceo_approver:
                    if company.company_ceo and company.company_ceo.id == self.env.user.id:
                        if record.request_status in show_final_approval and \
                                record.category_id.is_manual_approval is True:
                            r_status = True
                if record.category_id.is_hod_approver:
                    if employee.hod and employee.hod.user_id.id == self.env.user.id:
                        if record.request_status in show_final_approval and \
                                record.category_id.is_manual_approval is True:
                            r_status = True
                if record.category_id.is_manager_approver:
                    if employee.parent_id and employee.parent_id.user_id.id == self.env.user.id:
                        if record.request_status in show_final_approval:
                            r_status = True
            record.show_final_approval = r_status

    @api.depends('approver_ids.status')
    def _compute_user_status(self):
        for approval in self:
            approval.user_status = approval.approver_ids.filtered(
                lambda approver: approver.user_id == self.env.user).status

    @api.depends('approver_ids.status')
    def _compute_request_status(self):
        for request in self:
            status_lst = request.mapped('approver_ids.status')
            if not self.category_id.approval_budget_line:
                minimal_approver = request.approval_minimum if len(status_lst) >= request.approval_minimum else len(
                    status_lst)
            else:
                minimal_approver = self.minimal_approval
            print(minimal_approver)
            if request.category_id.is_manual_approval:
                if status_lst:
                    if status_lst.count('cancel'):
                        status = 'cancel'
                    elif status_lst.count('refused'):
                        status = 'refused'
                    elif status_lst.count('new'):
                        status = 'new'
                    elif status_lst.count('on_hold'):
                        status = 'on_hold'
                    else:
                        status = 'pending'
                else:
                    status = 'new'
                if request.final_approve is True:
                    status = 'approved'
            else:
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
                        if request.category_id.has_follower_after_approved:
                            ids = []
                            for record in request.category_id.followers.ids:
                                ids.append(record)
                            request.message_subscribe(ids)
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
            if employee.parent_id and employee.parent_id.user_id:
                new_users |= employee.parent_id.user_id

        if self.category_id.is_senior:
            if employee.senior and employee.senior.user_id:
                new_users |= employee.senior.user_id

        if self.category_id.is_supervisor:
            if employee.supervisor and employee.supervisor.user_id:
                new_users |= employee.supervisor.user_id

        if self.category_id.is_hod_approver:
            if employee.hod.user_id:
                new_users |= employee.hod.user_id
        if self.category_id.is_ceo_approver:
            company = self.env['res.company'].search([('id', '=', employee.company_id.id)], limit=1)
            if company.company_ceo:
                new_users |= company.company_ceo
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

    def action_withdraw(self, approver=None):
        self.final_approve = False
        if not isinstance(approver, models.BaseModel):
            approver = self.mapped('approver_ids').filtered(
                lambda approver: approver.user_id == self.env.user
            )
        approver.write({'status': 'pending'})

    def approval_action_final(self, approver=None):
        self.final_approve = True
        self.request_status = 'approved'
        if not isinstance(approver, models.BaseModel):
            approver = self.mapped('approver_ids').filtered(
                lambda approver: approver.user_id == self.env.user
            )
        approver.write({'status': 'approved'})
        self.sudo()._get_user_approval_activities(user=self.env.user).action_feedback()

    @api.onchange('amount')
    def _onchange_amount(self):
        if self.category_id.approval_budget_line:
            self.approver_ids = False
            new_users = self.category_id.user_ids
            current_users = self.approver_ids.mapped('user_id')
            employee_obj = self.env['hr.employee'].search([('user_id', '=', self.request_owner_id.id)])
            company_obj = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
            max_budget = 0
            minimal_approver = 0

            for record in self.category_id.approval_budget_line:
                if max_budget < record.max_budget:
                    max_budget = record.max_budget
            for record in self.category_id.approval_budget_line:
                if self.amount > max_budget:
                    self.minimal_approval = 3
                    if company_obj and company_obj.company_ceo:
                        new_users |= company_obj.company_ceo
                    if employee_obj and employee_obj.hod.user_id:
                        new_users |= employee_obj.hod.user_id
                    if employee_obj and employee_obj.parent_id.user_id:
                        new_users |= employee_obj.parent_id.user_id
                    break
                elif (self.amount <= record.max_budget) and (record.sequence_number == 1):
                    if employee_obj and employee_obj.parent_id.user_id:
                        new_users |= employee_obj.parent_id.user_id
                    break
                else:
                    self.minimal_approval = 2
                    if employee_obj and employee_obj.parent_id.user_id:
                        new_users |= employee_obj.parent_id.user_id
                    if employee_obj and employee_obj.hod.user_id:
                        new_users |= employee_obj.hod.user_id
                    break

            if new_users:
                for user in new_users - current_users:
                    self.approver_ids += self.env['approval.approver'].new({
                        'user_id': user.id,
                        'request_id': self.id,
                        'status': 'new'})


class ApprovalApprover(models.Model):
    _inherit = 'approval.approver'

    status = fields.Selection([
        ('new', 'New'),
        ('pending', 'To Approve'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('on_hold', ' On-Hold'),
        ('cancel', 'Cancel')], string="Status", default="new", readonly=True)
