from odoo import api, fields, models, _


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description="Appointment Records"
    _inherit="mail.thread"
    name=fields.Char(string='Order Reference', default='New')
    patient_id=fields.Many2one('hospital.patient',string='Patient',required=True)
    doctor_id=fields.Many2one('hospital.doctor',string='Doctor', required=True)
    age=fields.Integer(string='Age', related='patient_id.age',tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',String='Status')
    note=fields.Text(string='Description')
    date_appointment=fields.Date(string='Date')



    def action_confirm(self):
        self.state='confirm'


    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

