from odoo import models, fields, api

# Job Model
class Jobs(models.Model):
    _name = 'hr.customized.jobs'
    _description = 'Job Position'

    name = fields.Char(string='Job Title', required=True)
    description = fields.Text(string='Job Description')
    department_id = fields.Many2one('hr.customized.departments', string='Department', required=True)
    employee_ids = fields.One2many('hr.customized.employees', 'job_id', string='Employees')
    is_open = fields.Boolean(string='Is Open?', default=True)


    def jobs_xlsx_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url':f'/jobs/excel/report/{self.env.context.get("active_ids")}',
            'target':'new'
        }

    def jobs_xlsx_report_custom(self):
        return {
            'type': 'ir.actions.act_url',
            'url':f'/jobs/excel/report/customized/{self.env.context.get("active_ids")}',
            'target':'new'
        }

    # def delete_job(self):
    #     """Delete the selected applicant."""
    #     for record in self:
    #         record.unlink()

    # def update_job(self):
    #     """Update applicant logic (redirect to form view for editing)."""
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Update Job',
    #         'view_mode': 'form',
    #         'res_model': 'hr.job',
    #         'res_id': self.id,
    #         'target': 'new',
    #     }
