# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ApprovalBudget(models.Model):
    _name = 'approval.budget'

    name = fields.Char()
    budget_min = fields.Float()
    budget_max = fields.Float()
    approver = fields.Selection([
        ('manager', 'Manager'),
        ('head_deaprtment', 'Head Department'),
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
        inverse_name="request_id",)


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    @api.onchange('amount')
    def onchange_amount(self):
        if self.category_id.budget_lines:
            budget_line = self.env['approval.budget'].search([
                ('request_id', 'in', [self.category_id.id]),
                ('budget_min', '<=', self.amount),
                ('budget_max', '>=', self.amount)
            ])
            if budget_line:
                print(budget_line)
            else:
                print('No budget')
