# controllers/hospital_patient_dashboard.py
from datetime import datetime,timedelta
from odoo import http
from odoo.http import request

import logging

_logger = logging.getLogger(__name__)

class HospitalPatientDashboard(http.Controller):

    @http.route('/hospital/patient_dashboard/data', type='json', auth='public')
    def patient_dashboard_data(self,selected_data):

        _logger.info("###################### reached ##############")
        _logger.info("###################### reached ##############")
        _logger.info(selected_data)
        if int(selected_data)==0:
           selected_data=1
        patients = request.env['hospital.patient'].search([
            ('create_date','>',datetime.now()-timedelta(days=int(selected_data)))
        ])
        _logger.info("########################## date ##################")
        _logger.info(datetime.now()-timedelta(days=int(selected_data)))
        male_count = sum(1 for p in patients if p.gender == 'male')
        female_count = sum(1 for p in patients if p.gender == 'female')
        child_count = sum(1 for p in patients if p.is_child)
        _logger.info("###################### reached ##############")
        _logger.info(male_count)
        _logger.info(female_count)
        _logger.info(child_count)
        patients=len(patients)
        male_percent,female_percent,child_percent=0,0,0
        if male_count>0:
         male_percent=round((male_count/patients)*100,2) 
        if female_count>0:
            female_percent=round((female_count/patients)*100,2)
        if child_count>0:
         child_percent=round((child_count/patients)*100,2)
        values = {
            'total_patients': patients,
            'male_patient': male_count,
            'female_patient': female_count,
            'child_patient': child_count,
            'male_percent':male_percent,
            'female_percent':female_percent,
            'child_percent':child_percent,

        }
        return values
    
