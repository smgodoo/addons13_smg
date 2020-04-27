# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'

    privacy_visibility = fields.Selection([
        ('followers', 'Invited employees'),
        ('employees', 'All employees'),
        ('portal', 'Portal users and all employees'),
    ],
        string='Visibility', required=True,
        default='followers',
        help="Defines the visibility of the tasks of the project:\n"
             "- Invited employees: employees may only see the followed project and tasks.\n"
             "- All employees: employees may see all project and tasks.\n"
             "- Portal users and all employees: employees may see everything."
             "   Portal users may see project and tasks followed by.\n"
             "   them or by someone of their company.")
