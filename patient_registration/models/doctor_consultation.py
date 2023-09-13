from odoo import models, fields, api

class DoctorConsultation(models.Model):
    _name = 'doctor.consultation'
    _description = 'Doctor Consultation'

    
    op_no = fields.Char(string='OP No')
    date = fields.Date(string='Date')

    walk_in_patient_ids = fields.One2many('doctor.consultation.walk.in', 'consultation_id', string='Walk In Patients')
    patient_history_ids = fields.One2many('patient.history', 'consultation_id', string='Patients History')

    ############screen-body
    name = fields.Char(string='Name')
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    method = fields.Selection([
        ('', 'Select'),
        ('haemodialysis', 'Haemodialysis'),
        ('isolated_uf', 'Isolated UF'),
        ('sequential_uf', 'Sequential UF'),
        ('heamofiltration', 'Heamofiltration')
    ], string='Method', default='')
    indication = fields.Selection([
        ('', 'Select'),
        ('pulmonary_oedema', 'Pulmonary Oedema'),
        ('hyper_kalemia', 'Hyper Kalemia'),
        ('fluid_overload', 'Fluid Overload'),
        ('encephalopathy', 'Encephalopathy')
    ], string='Indication', default='')
    access = fields.Selection([
        ('', 'Select'),
        ('avf', 'AVF'),
        ('dlfc', 'DLFC'),
        ('dlsc', 'DLSC'),
        ('perm_cath', 'PERM CATH')
    ], string='Access')
    diagnosis = fields.Selection([
        ('', 'Select'),
    ], string='Access', default='')
    blood_flow = fields.Float(string='Blood Flow')
    dialyzer = fields.Char(string='Dialyzer')
    heparin_dosage = fields.Selection([
        ('', 'Select'),
        ('regular', 'Regular'),
        ('rigid', 'Rigid'),
        ('hep_free', 'HEP Free')
    ], string='Heparin Dosage', default='')
    uf_removal = fields.Float(string='UF Removal')
    pre_hd = fields.Float(string='Pre HD')
    post_hd = fields.Float(string='Post HD')
    time_started = fields.Datetime(string='Time Started')
    time_closed = fields.Datetime(string='Time Closed')
    priming_fluid = fields.Char(string='Priming Fluid')
    dialysate_flow = fields.Float(string='Dialysate Flow')

    #########screen-template
    template = fields.Selection([
        ('t1', 'Template 1'),
        ('t2', 'Template 2'),
        ('t3', 'Template 3'),
        ('t4', 'Template 4'),
        ('t5', 'Template 5'),
    ], string='Template', default='t1')
    

    #########screen-footer
    started_by = fields.Many2one('res.users', string='Started By')
    closed_by = fields.Many2one('res.users', string='Closed By')
    complication_note = fields.Selection([
        ('', 'Select'),
        ('bleeding', 'Bleeding'),
        ('hypotension', 'Hypotension'),
        ('hypertension', 'Hypertension'),
        ('cramps', 'Cramps'),
        ('others', 'Others')
    ], string='Complications during HD', default='')
    cleaning_fluid = fields.Selection([
        ('', 'Select'),
        ('saline', 'Saline'),
        ('hyperchloride', 'Hyperchloride'),
        ('formaline', 'Formaline'),
        ('h2o2', 'H2O2')
    ], string='Cleaning Fluid', default='')
    patient_is = fields.Char(string='Patient Is')
    next_hd_on = fields.Date(string='Next HD on')


class DoctorConsultationWalkIn(models.Model):
    _name = 'doctor.consultation.walk.in'
    
    consultation_id = fields.Many2one('doctor.consultation', string='Consultation')
    patient = fields.Char(string='Patient')
    op_no = fields.Char(string='OP No')
    time = fields.Char(string='Time')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in', 'In'),
    ], string='Status', default='draft')

class PatientHistory(models.Model):
    _name = 'patient.history'
    
    consultation_id = fields.Many2one('doctor.consultation', string='Consultation')
    date = fields.Date(string='Date')
    patient = fields.Char(string='Patient')

