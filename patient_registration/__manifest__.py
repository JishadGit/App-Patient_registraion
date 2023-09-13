{
    'name': 'Patient Registration',
    'version': '1.0',
    'description': 'patient registration',
    'summary': 'patient registration',
    'author': '',
    'category': '',
    'website': '',
    'license': 'LGPL-3',
    'category': 'Report',
    'depends': ['base'],
    'data': [
            'security/ir.model.access.csv',
            'views/assets.xml',
            'views/view.xml',
            'views/patient.xml',
            'views/patient_master.xml',
            'wizards/patient_appointment_report.xml',
            'reports/patient_appointment_report.xml',
            'reports/monthwise_patient_appointment_report.xml',
            'reports/detailed_monthwise_patient_appointment_report.xml',
            'reports/daywise_patient_appointment_report.xml',
            'reports/detailed_daywise_patient_appointment_report.xml',
            

            ],
    'auto_install': False,
    'application': True,
    'sequence': 2
}

