from odoo import http
from odoo.http import request
import io
import xlsxwriter
from ast import literal_eval

class XlsxCandidatesReport(http.Controller):

    @http.route('/candidate_reports/excel/report/<string:candidates_ids>', type='http', auth='user')
    def download_candidates_excel_report(self, candidates_ids):
        
        candidates_ids = request.env['hr.candidate'].browse(literal_eval(candidates_ids))

        print(candidates_ids)
        output = io.BytesIO()
        workbook =  xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Candidates')

        
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align':'center'})
        string_format = workbook.add_format({'border': 1, 'align':'center'})
        number_format = workbook.add_format({'border': 1, 'align':'center'})
        salary_format = workbook.add_format({'num_format': '$#####,##00.00' ,'border': 1, 'align':'center'})
        
        headers = ['Name', 'Email', 'Phone Number', 'Job', 'CV Score', 'CV Ranking']

        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num,header, header_format)

        row_num = 1
        for candidate in candidates_ids:
            worksheet.write(row_num, 0, candidate.partner_name, string_format)
            worksheet.write(row_num, 1, candidate.email_from, string_format)
            worksheet.write(row_num, 2, candidate.partner_phone, number_format)
            worksheet.write(row_num, 3, candidate.job_required_id.name, string_format)
            worksheet.write(row_num, 4, candidate.cv_score, number_format)
            worksheet.write(row_num, 5, candidate.cv_rank, string_format)
            row_num += 1

        workbook.close()
        output.seek(0)
        file_name = 'Candidates Report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformat-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename={file_name}')
            ]
        )

        
