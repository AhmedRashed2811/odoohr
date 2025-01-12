from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime
import base64
import pdfkit


class Employees(models.Model):
    _name = 'hr.employees'
    _description = 'Employees'

    name = fields.Char(string='Employee Name', required=True)
    marital_status = fields.Boolean(string='Is Married', required=True)
    department_id = fields.Many2one('hr.department', string="Department", ondelete='set null')
    job_id = fields.Many2one('hr.job', string="Job Title", ondelete='set null')
    manager_id = fields.Many2one('hr.employees', string="Manager", ondelete='set null')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    date_of_birth = fields.Date(string='Date of Birth')
    joining_date = fields.Date(string='Joining Date')
    salary = fields.Float(string='Salary')
    is_active = fields.Boolean(string='Is Active?', default=True)

    def delete_employee(self):
        """Delete the selected applicant."""
        for record in self:
            record.unlink()

    def update_employee(self):
        """Update applicant logic (redirect to form view for editing)."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Update Employee',
            'view_mode': 'form',
            'res_model': 'hr.employees',
            'res_id': self.id,
            'target': 'new',
        }

