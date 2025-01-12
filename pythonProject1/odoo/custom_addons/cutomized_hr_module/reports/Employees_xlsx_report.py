from odoo import http
from odoo.http import request
import io
import xlsxwriter
from ast import literal_eval

class XlsxEmployeesReport(http.Controller):

    @http.route('/emloyees/excel/report/<string:employees_ids>', type='http', auth='user')
    def download_employees_excel_report(self, employees_ids):
        
        employees_ids = request.env['hr.customized.employees'].browse(literal_eval(employees_ids))

        print(employees_ids)
        output = io.BytesIO()
        workbook =  xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Employees')

        
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align':'center'})
        string_format = workbook.add_format({'border': 1, 'align':'center'})
        number_format = workbook.add_format({'border': 1, 'align':'center'})
        salary_format = workbook.add_format({'num_format': '$#####,##00.00' ,'border': 1, 'align':'center'})
        
        headers = ['Name', 'Age', 'Job', 'Salary']

        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num,header, header_format)

        row_num = 1
        for employee in employees_ids:
            worksheet.write(row_num, 0, employee.name, string_format)
            worksheet.write(row_num, 1, employee.age, number_format)
            worksheet.write(row_num, 2, employee.job_id.name, string_format)
            worksheet.write(row_num, 3, employee.salary, salary_format)
            row_num += 1

        workbook.close()
        output.seek(0)
        file_name = 'Employees Report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformat-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename={file_name}')
            ]
        )

        
