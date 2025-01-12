from odoo import fields, models, api

class Applicants(models.Model):

    _name = "hr.applicants"
    _description = "This Model is for Applicants"


    name = fields.Char(string="Name", required = True, size = 100)
    age = fields.Integer(string="Age", required = True)
    phone_number = fields.Text(string="Phone Number", required = True, size = 15)
    degree = fields.Selection(string = "Degree", selection=[('high_School', 'High School'), ('bachelor', 'Bachelor'),("masters", "Masters")])
    experience_years = fields.Selection(string = "Years of Experience", selection=[("zero_two", "0-2"),("two_five", "2-5"),("five_plus", "5+")])
    field_of_study = fields.Text(string="Field of Study", required = True, size = 100)
    professional_job_title = fields.Text(string="Job Title", required = True, size = 100)
    marital_status = fields.Boolean(string="Is Married?", required=True)
    birth_date = fields.Date(string="Birth Date", required=True)
    resume_pdf = fields.Binary(string="Resume (PDF)", attachment=True)


    # name = fields.Char(string="Name", required = True, size = 100, tracking = True)
    # age = fields.Integer(string="Age", required = True, tracking = True)
    # phone_number = fields.Text(string="Phone Number", required = True, size = 15, tracking = True)
    # degree = fields.Selection(string = "Degree", selection=[('high_School', 'High School'), ('bachelor', 'Bachelor'),("masters", "Masters")], tracking = True)
    # experience_years = fields.Selection(string = "Years of Experience", selection=[("zero_two", "0-2"),("two_five", "2-5"),("five_plus", "5+")], tracking = True)
    # field_of_study = fields.Text(string="Field of Study", required = True, size = 100, tracking = True)
    # professional_job_title = fields.Text(string="Job Title", required = True, size = 100, tracking = True)
    # marital_status = fields.Boolean(string="Is Married?", required=True, tracking = True)
    # birth_date = fields.Date(string="Birth Date", required=True, tracking = True)
    # resume_pdf = fields.Binary(string="Resume (PDF)", attachment=True, tracking = True)


    
    # @api.model
    # def create(self, vals):
    #     return super(Applicants, self).create(vals)

    def delete_applicant(self):
        """Delete the selected applicant."""
        for record in self:
            record.unlink()

    def update_applicant(self):
        """Update applicant logic (redirect to form view for editing)."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Update Applicant',
            'view_mode': 'form',
            'res_model': 'hr.applicants',
            'res_id': self.id,
            'target': 'new',
        }
