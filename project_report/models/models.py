# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import datetime
import calendar
import re
import json

today = datetime.datetime.today()
TAG_RE = re.compile(r'<[^>]+>')


class ProjectProject(models.Model):
    _inherit = ['project.project']

    department_id_vt = fields.Many2many('hr.department', string="Department")


class ProjectPlan(models.Model):
    _inherit = 'planning.slot'

    def project_forecast_report_xlsx_action(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'project_report.project_forecast_xlsx',
            'model': 'planning.slot',
            'report_type': "xlsx",
        }

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
        a_dp = ('all', 'All Department')
        if self.env.user.has_group('project_owner_team.project_owner_team_group_project_see_all') or self.env.uid == 1:
            department_obj = self.env['hr.department'].search([])
        else:
            department_obj = self.env['hr.department'].search([('parent_id', '=', employee.department_id.id)])
        if department_obj:
            for record in department_obj:
                d_tp = ("{}".format(record.id), record.name)
                departments.append(d_tp)
        if self.env.user.has_group('project_owner_team.project_owner_team_group_project_see_all') or self.env.uid == 1:
            departments.append(a_dp)
        if options:
            options['selected_year'] = options['selected_year']
            if options.get('selected_department'):
                options['selected_department'] = options['selected_department']
        else:
            if self.env.user.has_group(
                    'project_owner_team.project_owner_team_group_project_see_all') or self.env.uid == 1:
                selected_dp = 'all'
            else:
                selected_dp = employee.department_id.id
            options = {
                'selected_year': today.year,
                'selected_department': selected_dp
            }
        options['list_year'] = list_year
        options['departments'] = departments
        options['month_list'] = month_list
        options['week_in_month'] = week_in_month

        project_forecasts = self.env['planning.slot'].search([])
        forecast_list = []
        forecast_dict = []
        forecast_data_ids = []
        if project_forecasts:
            for record in project_forecasts:
                project_year = fields.Date.from_string(record.end_datetime)
                if options['selected_department'] != 'all':
                    if int(options[
                               'selected_department']) in record.project_id.department_id_vt.ids and project_year.year == int(
                        options['selected_year']):
                        record_dict = {
                            'id': record.id,
                            'text': "{}".format(record.project_id.name),
                            'start_date': record.start_datetime,
                            'duration': 15,
                            'budget': record.project_id.project_budget
                        }
                        forecast_list.append(record_dict)
                        forecast_dict.append(record)
                        forecast_data_ids.append(record.id)
                else:
                    if options['selected_year']:
                        if project_year.year == int(options['selected_year']):
                            record_dict = {
                                'id': record.id,
                                'text': "{}".format(record.project_id.name),
                                'start_date': record.start_datetime,
                                'duration': 15,
                                'budget': record.project_id.project_budget
                            }
                            forecast_dict.append(record)
                            forecast_list.append(record_dict)
                            forecast_data_ids.append(record.id)
                    else:
                        record_dict = {
                            'id': record.id,
                            'text': "{}".format(record.project_id.name),
                            'start_date': record.start_datetime,
                            'duration': 15,
                            'budget': record.project_id.project_budget
                        }
                        forecast_dict.append(record)
                        forecast_list.append(record_dict)
                        forecast_data_ids.append(record.id)
        options['forecast_dict'] = forecast_dict
        options['forecast_ids'] = forecast_data_ids
        search_view_dict = {'options': options, 'context': self.env.context, 'data': forecast_list}
        templates = self.get_templates()
        html = self.env['ir.ui.view'].render_template(
            templates.get('main_template'), values=dict(search_view_dict))
        info = {
            'options': options,
            'context': self.env.context,
            'report_manager_id': 1,
            'footnotes': [],
            'forecast_list': forecast_list,
            'buttons': self.smg_vt_get_reports_buttons(),
            'main_html': html,
            'searchview_html': self.env['ir.ui.view'].render_template(templates.get('search_template'),
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

    def looking_week_in_month(self, dt):
        month_list = [
            [1, 2, 3, 4, 5, 6, 7],
            [8, 9, 10, 11, 12, 13, 14],
            [15, 16, 17, 18, 19, 20, 21],
            [22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
        ]
        result = 0
        date = fields.Date.from_string(dt)
        for (i, week) in enumerate(month_list, start=1):
            for j in week:
                if j == date.day:
                    result = i
                    break
        return result

    def date_range_to_write(self, week, dt):
        date = fields.Date.from_string(dt)
        project_static_title = 6
        number_col_in_month = 4
        column_index = project_static_title + (number_col_in_month * date.month)
        dc = number_col_in_month - week
        return column_index - dc

    def get_start_and_end_week_gap(self, start, end):
        print("{} : {}".format(start, end))
        if start and end:
            if start > 0 and end > 0:
                week_list = [i for i in range(start, end)]
                print(week_list)
                return week_list

    def remove_html_tag(self, text):
        return TAG_RE.sub('', text)

    def get_date_from_date(self, dt):
        date = fields.Date.from_string(dt)
        return date.day

    def smg_project_forecast_vt_export_xlsx(self, options):
        # print(options['forecast_ids'])
        forecast_ids = []
        forecasts = self.env['planning.slot'].search([('id', 'in', options['forecast_ids'])])
        for record in forecasts:
            forecast_ids.append(record.id)
        return self.env.ref('project_report.smg_project_forecast_vt_report_xlsx_filter').report_action([], data=options)

    def smg_vt_get_reports_buttons(self):
        return [{'name': _('Print Preview'), 'action': 'print_pdf', 'class': 'smg_project_forecast_hidden_button'},
                {'name': _('Export (XLSX)'), 'action': 'smg_project_forecast_vt_export_xlsx',
                 'class': 'o_project_forecast_vt_export_xlsx'}]