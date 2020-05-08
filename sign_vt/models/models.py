# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SignCategory(models.Model):
    _name = 'sign.category'

    name = fields.Char()


class SignTemplate(models.Model):
    _inherit = 'sign.template'

    category_id = fields.Many2one('sign.category')
