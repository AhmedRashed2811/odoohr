from odoo import http
from odoo.http import request
import io
import xlsxwriter
from ast import literal_eval

class XlsxJobsReport(http.Controller):

    @http.route('/jobs/excel/report/customized/<string:jobs_ids>', type='http', auth='user')
    def download_employees_excel_report(self, jobs_ids):
        
        jobs_ids = request.env['hr.customized.jobs'].browse(literal_eval(jobs_ids))

        output = io.BytesIO()
        workbook =  xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Jobs')

        
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align':'center'})
        string_format = workbook.add_format({'border': 1, 'align':'center'})
        number_format = workbook.add_format({'border': 1, 'align':'center'})
        salary_format = workbook.add_format({'num_format': '$#####,##00.00' ,'border': 1, 'align':'center'})
        
        headers = ['Job Title', 'Job Description']

        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num,header, header_format)

        row_num = 1
        for job in jobs_ids:
            worksheet.write(row_num, 0, job.name, string_format)
            worksheet.write(row_num, 1, job.description, number_format)
            row_num += 1

        workbook.close()
        output.seek(0)
        file_name = 'Jobs Report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformat-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename={file_name}')
            ]
        )