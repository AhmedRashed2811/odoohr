from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError
from datetime import date
from odoo.http import request

class Recruitment(models.Model):
    _inherit = ['hr.candidate', 'mail.thread', 'mail.activity.mixin']
    _description ="Candidate"
    _name = "hr.customized.candidates"
    
    cv_score = fields.Float(string = "CV Score")
    job_required_id = fields.Many2one('hr.customized.jobs',string="Job Applied")
    cv_rank = fields.Char(string = "CV Rank")
    cv = fields.Binary(string = "CV", attachment=True, required = True)
    active = fields.Boolean(default = True)
    email_from = fields.Char(string = "Email", required = True, tracking = 1)
    partner_phone = fields.Char(string = "Phone Number", required = True)
    partner_name = fields.Char(string = "Name", required = True)
    birthday = fields.Date(string ="Birth Date", required = True)
    age = fields.Integer(string  = "Age", compute = '_calculate_age', readonly= True)
    state = fields.Selection(selection=[('draft','Draft'),('interviewing', 'Interviewing'), ('hiring', 'Hiring')], default = 'draft')
    line_ids = fields.One2many('candidate.line', inverse_name='candidate_id')
    salary = fields.Float(string="Salary", required=False)
    image = fields.Binary(string="Personal Image", attachment=True, required = False)

    def change_state_to_interviewing(self):
        self.state = "interviewing"
        return 1

    def change_state_to_draft(self):
        self.state = "draft"
        return 1

    def open_hiring_view(self):
        return {
                'type': 'ir.actions.act_window',
                'name': 'Hiring New Employee',
                'view_mode': 'form',
                'view_id': self.env.ref('cutomized_hr_module.candidates_hiriring_view_form').id,
                'res_model': 'hr.customized.candidates',
                'res_id': self.id,
                'target': 'new',
            }

    def change_state_to_hired(self):
        """Change the candidate state to 'hiring', create an employee, and delete the candidate."""

        if self.salary == 0:
            raise ValidationError("Salary Cann't be 0!")
        
        if not self.image:
            raise ValidationError("Personal Image is not Set!")

        self.ensure_one()
        self.state  = 'hiring'

        # Ensure employee creation
        employee_vals = {
            'name': self.partner_name,
            'email': self.email_from,
            'phone': self.partner_phone,
            'birth_date': self.birthday,
            'age': self.age,
            'salary': self.salary,
            'cv_file': self.cv,
            'cv_filename': self.cv or f"{self.partner_name}_CV.pdf",
            'job_id': self.job_required_id.id,
            'is_active': True,
            'image': self.image,
        }

        new_employee = self.env['hr.customized.employees'].create(employee_vals)
        if not new_employee:
            raise ValidationError("Failed to create employee record. Please check the input data.")

        self.unlink()

        # Trigger a notification for the user
        self.env['bus.bus']._sendone(
            self.env.user.partner_id,
            'simple_notification',
            {
                'title': "New Employee is Created Successfully!",
                'sticky': False,  # Notification disappears after a few seconds
                'type': 'success',   # 'info', 'warning', or 'danger'
                'duration': 5000
            }
        )

        # Redirect to the employee list view
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.customized.candidates',
            'view_mode': 'list,form',
            'target': 'current',
        }


        # Delete the candidate record after returning the action
        
        return action

           
    def change_state_to_reject(self):
        res = super(Recruitment, self).unlink()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.customized.candidates',
            'view_mode': 'list,form', 
            'target': 'current',
        }
    
    @api.constrains('email_from')
    def _check_email(self):
        for rec in self:
            if rec.email_from:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, rec.email_from):
                    raise ValidationError('Invalid Email!')

    @api.constrains('partner_phone')
    def _check_phone(self):
        for rec in self:
            if rec.partner_phone:
                phone_regex = r'^(0)?\d{7,}$'
                if not re.match(phone_regex, rec.partner_phone):
                    raise ValidationError('Invalid Phone Number!')

    @api.onchange('birthday')
    def _check_birthday(self):
        for rec in self:
            if rec.birthday:
                today = date.today()
                # Calculate the age based on the birthday
                age = today.year - rec.birthday.year - ((today.month, today.day) < (rec.birthday.month, rec.birthday.day))
                # Validate the age range
                if age < 21 or age > 45:
                    request.env['bus.bus']._sendone(
                        self.env.user.partner_id,
                        'simple_notification',
                        {
                            'title': "Invalid Birthday",
                            'message': "The candidate age must be between 21 and 45 years old.",
                            'type': 'warning',  # Can be 'info', 'warning', or 'danger'
                        }
                    )
                    # Clear the invalid birthday
                    rec.birthday = False

    
    _sql_constraints = [
        ('unique_email', 'unique(email_from)', 'Email Already Exists!'),
        ('unique_phone', 'unique(partner_phone)', 'Phone Number Already Exists!')
    ]

    
    def evaluate_CVs_AI(self):

        # Trigger a notification for the user
        self.env['bus.bus']._sendone(
            self.env.user.partner_id,
            'simple_notification',
            {
                'title': "AI Evaluation",
                'message': "Please Wait While the AI Evaluates the CVs",
                'sticky': False,  # Notification disappears after a few seconds
                'type': 'info',   # 'info', 'warning', or 'danger'
                'duration': 10000
            }
        )
        
        
        return {
            'type': 'ir.actions.act_url',
            'url':f'/applicants/evaluate/{self.env.context.get("active_ids")}',
            'target': 'self',
        }
        
    
    def candidates_xlsx_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url':f'/candidates/excel/report/{self.env.context.get("active_ids")}',
            'target':'new'
        }


    def candidate_cv_download(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/candidate/cv/download/{self.id}',
            'target': 'self'
        }


    @api.depends('birthday')
    def _calculate_age(self):
        for record in self:
            if record.birthday:
                today = date.today()
                birth_date = record.birthday
                # Calculate age in full years
                record.age = today.year - birth_date.year - (
                    (today.month, today.day) < (birth_date.month, birth_date.day)
                )
            else:
                record.age = 0

    
class RecruitmentLines(models.Model):
    _name = "candidate.line"

    candidate_id = fields.Many2one('hr.customized.candidates')
    study  = fields.Char(string = "Study")
    lives_in = fields.Char(string = "City")
    
