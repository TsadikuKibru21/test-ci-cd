
from odoo import api, fields, models, _
from odoo import api, fields, models
from odoo.service import db
from odoo.exceptions import UserError

class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description="Create Appointment Wizard"
    date_appointment=fields.Date(String='Date',required=False)
    patient_id=fields.Many2one('hospital.patient',string='Patient')
    doctor_id=fields.Many2one('hospital.doctor',string='Doctor')

    def action_create_appointment(self):
        print('Button is Clicked')
        vals= {
            'patient_id':self.patient_id.id,
            'doctor_id':self.doctor_id.id,
            'date_appointment':self.date_appointment
        }
        appointment_rec=self.env['hospital.appointment'].create(vals)

        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
            'target':'new',
        }
    def action_view_appointment(self):
        action=self.env.ref('Hospital_management.action_hospital_appointment').read()[0]
        action['domain']=[('patient_id','=',self.patient_id.id)]
        return action



# db_create_wizard/wizard/db_create_wizard.py



class DbCreateWizard(models.TransientModel):
    _name = 'db.create.wizard'
    _description = 'Wizard to Create a New Database'

    db_name = fields.Char(string="Database Name", required=True)
    admin_user = fields.Char(string="Admin User", required=True, default='admin')
    admin_password = fields.Char(string="Admin Password", required=True)

    def create_database(self):
        """Create a new Odoo database."""
        db_name = self.db_name
        admin_user = self.admin_user
        admin_password = self.admin_password

        # Check if database already exists
        if db_name in db.list_dbs():
            raise UserError("Database with this name already exists.")

        # Create the database
        try:
            db.exp_create_database(db_name, admin_password,demo=False, lang='en_US')
            self.env.cr.commit()  # Commit creation to the DB
        except Exception as e:
            raise UserError(f"Failed to create database: {e}")

        # Confirm success
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'params': {'message': f"Database '{db_name}' created successfully!"},
        }
