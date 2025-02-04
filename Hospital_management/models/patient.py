from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import docker
import os
import subprocess
from odoo.service import db
from odoo.exceptions import UserError

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Patient Records"
    _inherit = "mail.thread"

    name = fields.Char(String='Name', required=True, tracking=True,state={'confrim':[('readonly',True)],'done':[('readonly',True)],'cancel':[('readonly',True)]})
    age = fields.Integer(String='Age', tracking=True)
    is_child = fields.Boolean(String='Is Child ?', tracking=True)
    note = fields.Text(String='Notes')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], String='Gender', tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')],
                             default='draft', String='Status',  group_expand='_read_group_state_ids')
    capitalized_name = fields.Char(String='Capitalized_Name', compute='_compute_capitalized_name', store=True)
    ref = fields.Char(String='Reference', default=lambda self: _('New'))
    responsible_id = fields.Many2many('res.partner', string='Responsible')
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')
    image = fields.Binary(string='Patient Image')
    @api.model
    def _read_group_state_ids(self, states, domain, order):
        # Dynamically include all possible states in Kanban view
        return [state for state, _ in self._fields['state'].selection]

    def get_patient_dashboard_data(self):
        male_count = self.search_count([('gender', '=', 'male')])
        female_count = self.search_count([('gender', '=', 'female')])
        child_count = self.search_count([('is_child', '=', True)])
        total_patients = self.search_count([])

        return {
            'male_count': male_count,
            'female_count': female_count,
            'child_count': child_count,
            'total_patients': total_patients,
        }



# class DbCreateWizard(models.TransientModel):
#     _name = 'db.create.wizard'
#     _description = 'Wizard to Create a New Database'

#     db_name = fields.Char(string="Database Name", required=True)
#     admin_user = fields.Char(string="Admin User", required=True, default='admin')
#     admin_password = fields.Char(string="Admin Password", required=True)

    def create_database(self):
        """Create a new Odoo database."""
        db_name = "testdb1"
        admin_user = "admin"
        admin_password = "admin"

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

    def action_confirm(self):
        for i in self:
            i.state = 'confirm'

    def action_cancel(self):
        for i in self:
            i.state = 'cancel'

    def action_draft(self):
        for i in self:
            i.state = 'draft'

    def action_done(self):
        for i in self:
            i.state = 'done'
    def action_create_docker_image(self):

         # Docker command to build an image
        try:
            # Pull Odoo image
            password = "  "
            
            # odoo_pull = subprocess.run(['docker', 'pull', 'odoo:16'], capture_output=True, text=True)
            # if odoo_pull.returncode != 0:
            #     raise ValidationError(f"Odoo pull error: {odoo_pull.stderr}")
            
            # Pull PostgreSQL image
            # postgres_pull = subprocess.run(['docker', 'pull', 'postgres:12'], capture_output=True, text=True)
            # if postgres_pull.returncode != 0:
            #     raise ValidationError(f"Postgres pull error: {postgres_pull.stderr}")
            
            # # Run PostgreSQL container
            # postgres_run = subprocess.run([
            #     'docker', 'run', '--name', 'postgres_containers',
            #     '-e', 'POSTGRES_USER=odoo',
            #     '-e', 'POSTGRES_PASSWORD=odoo',
            #     '-e', 'POSTGRES_DB=odoo',
            #     '-d', 'postgres:12'
            # ], capture_output=True, text=True)
            # if postgres_run.returncode != 0:
            #     raise ValidationError(f"Postgres run error: {postgres_run.stderr}")
            
            # Run Odoo container
            odoo_run = subprocess.run([
                'docker', 'run', '--name', 'odoo_containerss',
                '--link', 'postgres_container:db',
                '-p', '8065:8069',
                '-d', 'odoo:16'
            ], capture_output=True, text=True)
            if odoo_run.returncode != 0:
                raise ValidationError(f"Odoo run error: {odoo_run.stderr}")
            
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        except Exception as e:
            raise ValidationError(f"Error: {str(e)}")

    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    @api.model_create_multi
    def create(self, varls_list):
        for var in varls_list:
            var['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(varls_list)

    @api.constrains('is_child', 'age')
    def _check_child_age(self):
        for rec in self:
            if rec.is_child and rec.age == 0:
                raise ValidationError(_("Age has to be recorded"))

    @api.depends('name')
    def _compute_capitalized_name(self):
        for rec in self:
            if rec.name:
                rec.capitalized_name = rec.name.upper()
            else:
                rec.capitalized_name = ''

    @api.onchange('age')
    def _onchange_age(self):
        if self.age <= 10:
            self.is_child = True
        else:
            self.is_child = False

    @api.model
    def default_get(self, fields):
        res = super(HospitalPatient, self).default_get(fields)
        res['state'] = 'confirm'
        res['age'] = 20
        return res
