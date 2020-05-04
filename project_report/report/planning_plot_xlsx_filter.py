from odoo import api, fields, models, _
import calendar
import datetime
import logging
import re
import json

_logger = logging.getLogger(__name__)
try:
    import xlsxwriter
except ImportError:
    _logger.debug('Can not import xlsxwriter.')
calendar.setfirstweekday(6)

TAG_RE = re.compile(r'<[^>]+>')


class ProjectForecastXlsx(models.AbstractModel):
    _name = 'report.project_report.project_forecast_xlsx_filter'
    _inherit = 'report.project_report.abstract'

    def find_day_in_week(self, week_in_month, looking_value):
        result = 0
        for (i, week) in enumerate(week_in_month, start=1):
            for j in week:
                if j == looking_value.day:
                    result = i
                    break
        return result

    def remove_html_tag(self, text):
        return TAG_RE.sub('', text)

    def find_day_in_week(self, numbers, looking_value):
        result = 0
        for (i, week) in enumerate(numbers, start=1):
            for j in week:
                if j == looking_value.day:
                    result = i
                    break
        return result

    def find_column_write_dateline(self, week, dt):
        project_static_title = 6
        number_col_in_month = 4
        column_index = project_static_title + (number_col_in_month * dt.month)
        dc = number_col_in_month - week
        return column_index - dc

    def generate_forecast_xlsx_report(self, workbook, data, partners):
        month_head_color_format = '#203764'
        static_head_color_format = '#F8C43C'
        today = datetime.datetime.today()
        options = json.loads(data.get('options'))
        if options.get('selected_department') != 'all':
            department_id = self.env['hr.department'].search([('id', '=', options.get('selected_department'))])
            department_title = department_id.name
        else:
            department_title = 'All Department'

        project_forecasts = self.env['planning.slot'].search([('id', 'in', options.get('forecast_ids'))])

        week_in_month = ['W1', 'W2', 'W3', 'W4']
        static_head_title = ['SUB DEPARTMENT', 'ACTIVITY', 'APPOINT TO', 'SUMMARY', 'BUDGET', 'NOTES']
        sheet = workbook.add_worksheet('Timings and Budget')

        head_title_format = workbook.add_format({
            'bg_color': static_head_color_format,
            'bold': True,
            'font_color': '#000000',
            'align': 'center',
            'valign': 'vcenter',
        })
        month_title_format = workbook.add_format({
            'bg_color': month_head_color_format,
            'font_color': '#ffffff',
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
        })
        project_title_format = workbook.add_format({
            'bg_color': static_head_color_format,
            'bold': True,
            'valign': 'vcenter',
            'text_wrap': True,
            'indent': 1,
        })
        project_budget_format = workbook.add_format({
            'num_format': '$#,##0.00',
            'bg_color': static_head_color_format,
            'bold': True,
            'valign': 'vcenter',
            'text_wrap': True,
            'indent': 1,
        })
        currency_format = workbook.add_format({
            'num_format': '$#,##0.00',
            'bold': True,
            'valign': 'vcenter',
            'text_wrap': True,
            'indent': 1,
        })
        normal_cell_format = workbook.add_format({
            'valign': 'vcenter',
            'text_wrap': True,
            'indent': 1,
        })
        department_cell_format = workbook.add_format({
            'valign': 'vcenter',
            'indent': 1,
            'text_wrap': True,
        })
        date_line_format = workbook.add_format({
            'bg_color': static_head_color_format,
            'valign': 'vcenter',
            'indent': 1,
        })
        date_line_blank_format = workbook.add_format({
            'bg_color': static_head_color_format,
        })
        days_in_month = [
            [1, 2, 3, 4, 5, 6, 7],
            [8, 9, 10, 11, 12, 13, 14],
            [15, 16, 17, 18, 19, 20, 21],
            [22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
        ]

        start_row = 7
        week_column_index = len(static_head_title)
        number_month_in_year = 12
        number_week_in_month = 4
        total_column = len(static_head_title) + (number_month_in_year * number_week_in_month)
        sheet.write(0, 0, '[{} {} BUDGET + TIMINGS'.format(department_title, today.year))
        sub_title = "- [Explanatory notes] - This calendar is dynamic and should be updated throughout the year as " \
                    "more opportunities arise - Each activity should also have a plan/ proposal on how we plan to " \
                    "activate "
        from_column_letter = xlsxwriter.utility.xl_col_to_name(0)
        last_column_letter = xlsxwriter.utility.xl_col_to_name(total_column)
        sheet.merge_range("{}{}:{}{}".format(from_column_letter, 2, last_column_letter, 5), sub_title,
                          normal_cell_format)
        start_column = 0
        static_head_row = 0
        for head in static_head_title:
            sheet.merge_range("{}{}:{}{}".format(
                xlsxwriter.utility.xl_col_to_name(start_column),
                start_row + 1,
                xlsxwriter.utility.xl_col_to_name(start_column),
                start_row + 2),
                head, head_title_format
            )
            sheet.set_column(start_column, start_column, 19)
            start_column += 1

        for month in range(1, 13):
            sheet.set_row(start_row, 24)
            from_column_letter = xlsxwriter.utility.xl_col_to_name(start_column)
            last_column_letter = xlsxwriter.utility.xl_col_to_name(len(week_in_month) + (start_column - 1))
            sheet.merge_range("{}{}:{}{}".format(
                from_column_letter, start_row + 1,
                last_column_letter, start_row + 1),
                calendar.month_name[month], month_title_format)
            start_column += len(week_in_month)

            for week in week_in_month:
                sheet.write(start_row + 1, week_column_index, week, month_title_format)
                week_column_index += 1
        freeze_column_index = start_row + 3
        sheet.freeze_panes("{}{}".format(
            xlsxwriter.utility.xl_col_to_name(len(static_head_title)),
            freeze_column_index
        ))

        start_record_row = 9
        start_record_column = 0
        if project_forecasts:
            for forecast in project_forecasts:
                department_list = [dp.name for dp in forecast.project_id.department_id_vt if
                                   forecast.project_id.department_id_vt]
                date_start = fields.Date.from_string(forecast.start_datetime)
                end_date = fields.Date.from_string(forecast.end_datetime)
                start_week = self.find_day_in_week(days_in_month, date_start)
                end_week = self.find_day_in_week(days_in_month, end_date)
                forecast_date_start = self.find_column_write_dateline(start_week, date_start)
                forecast_date_end = self.find_column_write_dateline(end_week, end_date)
                # sheet.set_row(start_record_row, 22)
                sheet.write(start_record_row, start_record_column, ', '.join(department_list), department_cell_format)
                sheet.write(start_record_row, start_record_column + 1, forecast.project_id.display_name,
                            normal_cell_format)
                sheet.write(start_record_row, start_record_column + 2, forecast.employee_id.display_name,
                            normal_cell_format)
                if forecast.project_id.project_description:
                    sheet.write(start_record_row, start_record_column + 3,
                                self.remove_html_tag(forecast.project_id.project_description),
                                normal_cell_format)
                if forecast.project_id.project_budget:
                    sheet.write(start_record_row, start_record_column + 4,
                                forecast.project_id.project_budget,
                                normal_cell_format)
                if forecast.project_id.project_note:
                    sheet.write(start_record_row, start_record_column + 5, forecast.project_id.project_note,
                                normal_cell_format)
                if forecast_date_start == forecast_date_end:
                    sheet.write(start_record_row, forecast_date_start - 1,
                                "{}-{}".format(date_start.day, end_date.day), date_line_format)
                else:
                    sheet.write(start_record_row, forecast_date_start - 1, "{}".format(date_start.day),
                                date_line_format)
                    for i in range(forecast_date_start, forecast_date_end):
                        if i == forecast_date_end - 1:
                            sheet.write(start_record_row, i, end_date.day, date_line_format)
                        else:
                            sheet.write(start_record_row, i, None, date_line_blank_format)
                start_record_row += 1
