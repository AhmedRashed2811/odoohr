import re
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Employees(models.Model):
    _name = "hr.customized.employees"
    _description = "Employees Data"
   

    name = fields.Char(string="Name", required=True, size=100)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone", required=True)
    birth_date = fields.Date(string="Birth Date", required=True)
    age = fields.Integer(string="Age", compute="_compute_age", readonly=True)
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string="Gender")
    marital_status = fields.Boolean(string="Is Married?")
    address = fields.Text(string="Address")
    joining_date = fields.Date(string="Joining Date", default=fields.Datetime.now)
    salary = fields.Float(string="Salary", required=True)
    cv_file = fields.Binary(string="CV File", attachment=True)
    
    cv_filename = fields.Char(string="CV Filename")
    image = fields.Binary(string="Personal Image", attachment=True)
    is_active = fields.Boolean(string="Is Active?", default=True)

    department_id = fields.Many2one('hr.customized.departments', string="Department", ondelete='set null')
    job_id = fields.Many2one('hr.customized.jobs', string="Job Title", ondelete='set null')
    manager_id = fields.Many2one('hr.customized.employees', string="Manager", ondelete='set null')

    @api.depends('birth_date')
    def _compute_age(self):
        """Calculate the age based on birth date."""
        for rec in self:
            if rec.birth_date:
                today = fields.Date.today()
                rec.age = today.year - rec.birth_date.year - (
                    (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, rec.email):
                    raise ValidationError('Invalid Email!')

    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age not in range(21, 45):
                raise ValidationError('Age must be between 21 and 45!')
    # @api.model_create_multi
    # def create(self, vals):
    #     res = super(Employees, self).create(vals)
    #     return res

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None):
        res = super(Employees, self)._search(domain, offset=0, limit=None, order=None)
        return res

    def write(self, vals):
        res = super(Employees, self).write(vals)
        return res


    def update_employee(self):
        
        """Update applicant logic (redirect to form view for editing)."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Update Employee',
            'view_mode': 'form',
            'res_model': 'hr.customized.employees',
            'res_id': self.id,
            'target': 'new',
        }
    

    def unlink(self):
        res = super(Employees, self).unlink()
        return res

    def employees_xlsx_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url':f'/emloyees/excel/report/{self.env.context.get("active_ids")}',
            'target':'new'
        }


    