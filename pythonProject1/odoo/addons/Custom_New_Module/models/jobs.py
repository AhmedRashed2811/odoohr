from odoo import models, fields, api

# Job Model
class Jobs(models.Model):
    _name = 'hr.job'
    _description = 'Job Position'

    name = fields.Char(string='Job Title', required=True)
    description = fields.Text(string='Job Description')
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    employee_ids = fields.One2many('hr.employees', 'job_id', string='Employees')
    is_open = fields.Boolean(string='Is Open?', default=True)

    def delete_job(self):
        """Delete the selected applicant."""
        for record in self:
            record.unlink()

    def update_job(self):
        """Update applicant logic (redirect to form view for editing)."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Update Job',
            'view_mode': 'form',
            'res_model': 'hr.job',
            'res_id': self.id,
            'target': 'new',
        }
