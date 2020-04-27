# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import datetime
import calendar
import re

today = datetime.datetime.today()


class ProjectPlan(models.Model):
    _inherit = 'planning.slot'

    def get_templates(self):
        return {
            'main_template': 'project_report.main_template',
            'search_template': 'project_report.search_template'
        }

    def get_report_informations(self, options):
        list_year = [(i, i) for i in range(2020, 2030)]
        month_list = [(i, calendar.month_name[i]) for i in range(1, 13)]
        week_in_month = ['W1', 'W2', 'W3', 'W4']
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        departments = []
        if self.env.uid == 2:
            department_obj = self.env['hr.department'].search([])
        else:
            department_obj = self.env['hr.department'].search([('parent_id', '=', employee.department_id.id)])
        if department_obj:
            for record in department_obj:
                d_tp = ("{}".format(record.id), record.name)
                departments.append(d_tp)
        if options:
            options['selected_year'] = options['selected_year']
            if options.get('selected_department'):
                options['selected_department'] = options['selected_department']
        else:
            options = {
                'selected_year': today.year,
                'selected_department': employee.department_id.id
            }
        options['list_year'] = list_year
        options['departments'] = departments
        options['month_list'] = month_list
        options['week_in_month'] = week_in_month
        search_view_dict = {'options': options, 'context': self._context}
        templates = self.get_templates()
        html = self.env['ir.ui.view'].render_template(
            templates.get('main_template'), values=dict(search_view_dict)
        )
        info = {
            'options': options,
            'context': self._context,
            'report_manager_id': 1,
            'footnotes': [],
            'buttons': self.get_report_buttons(),
            'main_html': html,
            'searchview_html': self.env['ir.ui.view'].render_template(
                templates.get('search_template'),
                values=search_view_dict),
        }
        return info

    def get_report_buttons(self):
        return [{'name': _('Print Preview'), 'action': 'print_pdf', 'class': 'smg_project_forecast_hidden_button'},
                {'name': _('Export (XLSX)'), 'action': 'smg_project_forecast_vt_export_xlsx',
                 'class': 'o_project_forecast_vt_export_xlsx'}]

    def get_html_footnotes(self, footnotes):
        template = self._get_templates().get('footnotes_template', 'account_reports.footnotes_template')
        rcontext = {'footnotes': footnotes, 'context': self.env.context}
        html = self.env['ir.ui.view'].render_template(template, values=dict(rcontext))
        return html

    # TO BE OVERWRITTEN
    def _get_templates(self):
        return {
            'main_template': 'account_reports.main_template',
            'main_table_header_template': 'account_reports.main_table_header',
            'line_template': 'account_reports.line_template',
            'footnotes_template': 'account_reports.footnotes_template',
            'search_template': 'account_reports.search_template',
        }