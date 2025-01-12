from odoo import http
from odoo.http import request
import os
import xlsxwriter
from ast import literal_eval

class XlsxJobsReport(http.Controller):

    @http.route('/jobs/excel/report/<string:jobs_ids>', type='http', auth='user')
    def save_employees_excel_report(self, jobs_ids):
        
        jobs_ids = request.env['hr.customized.jobs'].browse(literal_eval(jobs_ids))

        # Define the path to the data folder in the root directory
        data_folder_path = os.path.join(os.getcwd(), 'odoo','custom_addons', 'cutomized_hr_module','data')
        os.makedirs(data_folder_path, exist_ok=True)  # Create the data folder if it doesn't exist
        file_path = os.path.join(data_folder_path, 'Jobs_Report.xlsx')

        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet('Jobs')

        # Define formatting for the Excel file
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
        string_format = workbook.add_format({'border': 1, 'align': 'center'})
        number_format = workbook.add_format({'border': 1, 'align': 'center'})

        # Define headers
        headers = ['Job Title', 'Job Description']

        # Write headers
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

        # Write job data
        row_num = 1
        for job in jobs_ids:
            worksheet.write(row_num, 0, job.name, string_format)
            worksheet.write(row_num, 1, job.description, number_format)
            row_num += 1

        workbook.close()

        return f"The Excel report has been successfully saved to {file_path}"
