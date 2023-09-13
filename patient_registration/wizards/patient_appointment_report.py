from odoo import fields, models

class PatientAppointmentReport(models.TransientModel):
    _name = "patient.appointment.report.wizard"
    _description = "Patient Appointment Report Wizard"

    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")

    radio_button = fields.Selection([
        ('01', 'Monthwise Report'),
        ('02', 'Daywise Report'),
    ], string='Choose')

    detailed_report = fields.Boolean('Detailed Report')

    def generate_report(self):
        domain = []
        if self.from_date:
            domain.append(('create_date', '>=', self.from_date))
        if self.to_date:
            domain.append(('create_date', '<=', self.to_date))

        appointments = self.env['patient'].search_read(domain)

        # Dictionary to hold aggregated data for each day
        dates = {}

        # Dictionary to hold aggregated data for each month
        months = {}

        # List to hold detailed data for each appointment
        appointments_list = []

        for appointment in appointments:
            create_date = appointment['create_date'].date()
            if create_date not in dates:
                dates[create_date] = {
                    'date': create_date,
                    'appointments': [],
                    'count': 0,
                }
            dates[create_date]['appointments'].append(appointment)
            dates[create_date]['count'] += 1

            month_key = (create_date.year, create_date.month)
            if month_key not in months:
                months[month_key] = {
                    'year': create_date.year,
                    'month': create_date.month,
                    'appointments': [],
                    'count': 0,
                }
            months[month_key]['appointments'].append(appointment)
            months[month_key]['count'] += 1
            
            # Append appointment details to the list
            appointments_list.append(appointment)

        # Sort the appointments data based on the create date
        sorted_appointments = sorted(appointments_list, key=lambda x: x['create_date'])

        data = {
            'months': list(months.values()),  # Convert dictionary values to a list
            'dates': list(dates.values()),  # Convert dictionary values to a list
            'appointments': sorted_appointments,
            'from_date': self.from_date.strftime('%Y-%m-%d') if self.from_date else '',
            'to_date': self.to_date.strftime('%Y-%m-%d') if self.to_date else '',
        }
        if self.detailed_report:
        # Choose report name based on the selected radio button option
            if self.radio_button == '01':
                report_name = 'patient_registration.detailed_monthwise_patient_appointment_report_action'
            elif self.radio_button == '02':
                report_name = 'patient_registration.detailed_daywise_patient_appointment_report_action'
            else:
                report_name = 'patient_registration.patient_appointment_report_action'
        else:
            if self.radio_button == '01':
                report_name = 'patient_registration.monthwise_patient_appointment_report_action'
            elif self.radio_button == '02':
                report_name = 'patient_registration.daywise_patient_appointment_report_action'
            else:
                report_name = 'patient_registration.patient_appointment_report_action'
        # Return the report action
        return self.env.ref(report_name).report_action(self, data=data)
