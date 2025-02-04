{
    'name':'Hospital Management System',
    'version': '1.0.0',
    'summary':'Hospital management',
    'author': 'tsadiku',
    'website':'tsadiku.com',
    'desription':'Hospital',
    'depends':['mail','sale'],
    'data':[
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'data/demo_data.xml',
        'wizard/create_appointment_view.xml',
        # 'wizard/db_create_wizard_view.xml',

        
        'report/report.xml',
        'report/patient_details_template.xml',
        'views/menu.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/appointment.xml',
        # 'views/hospital_patient_dashboard.xml'
        # 'views/template.xml'
],
'assets': {
        'web.assets_backend': [
            'Hospital_management/static/src/components/**/*.js',
            'Hospital_management/static/src/components/**/*.xml',
            'Hospital_management/static/src/components/**/*.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1
}
