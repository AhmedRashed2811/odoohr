from odoo import models, fields, api

# Department Model
class Departments(models.Model):
    _name = 'hr.customized.departments'
    _description = "All company's departments"

    name = fields.Char(string='Department Name', required=True)
    manager_id = fields.Many2one('hr.customized.employees', string='Manager')
    employee_ids = fields.One2many('hr.customized.employees', 'department_id', string='Employees')
    job_ids = fields.One2many('hr.customized.jobs', 'department_id', string='Jobs')

    # def delete_department(self):
    #     """Delete the selected applicant."""
    #     for record in self:
    #         record.unlink()

    # def update_department(self):
    #     """Update applicant logic (redirect to form view for editing)."""
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Update Department',
    #         'view_mode': 'form',
    #         'res_model': 'hr.department',
    #         'res_id': self.id,
    #         'target': 'new',
    #     }
