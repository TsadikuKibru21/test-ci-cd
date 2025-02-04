from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class Hospital(http.Controller):

    @http.route('/hospital/patient/', website=True, auth='public')
    def hospital_patient(self,**kwargs):
        try:
            patients = request.env['hospital.patient'].search([])
            
            return request.render("Hospital_management.patients_page", {"patients": patients})
        except Exception as e:

            _logger.error("Error fetching patients: %s", e)
            return request.render("error_template", {"error_message": str(e)})

import json
class Patient(http.Controller):

    @http.route('/patient/patient/', website=True, auth='public', type='http', methods=['GET'])
    def hospital_patient(self):
        patients = request.env['hospital.patient'].search([])

        patient_data = []
        for pat in patients:
            patient_data.append({
                'id': pat.id,
                'name': pat.name,
                'age': pat.age,
            })
        return request.make_response(
            headers={'Content-Type': 'application/json'},
            data=json.dumps(patient_data)
        )
        
class PatientPost(http.Controller):
    @http.route('/patient/hospital/',website=True,auth='public',type='http',methods=['POST'])
    def hospital_patient_post(self):
        patient_data = request.jsonrequest
        
        new_patient = request.env['hospital.patient'].create({
            'name': patient_data['name'],
            'age': patient_data['age'],
        })

        response_data = {
            'message': 'Patient created successfully',
            'patient': {
                'id': new_patient.id,
                'name': new_patient.name,
                'age': new_patient.age,
            }
        }
        return request.make_response(
            headers={'Content-Type': 'application/json'},
            data=json.dumps(response_data),
            status=200
        )
    
        

