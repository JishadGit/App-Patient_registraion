from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class Patient(models.Model):
    _name = "patient"
    _description = "Patient Appointment Form"
    
    reg_type = fields.Selection([
        ('new', 'New'),
        ('existing', 'Existing')
    ], string='Reg No', required=True, default='new')
    reg_no = fields.Char(string='Reg No', readonly=True)
    
    patient_type = fields.Selection([
        ('mr', 'Mr.'),
        ('mrs', 'Mrs.'),
        ('ms', 'Ms.'),
        ('newborn', 'New Born.'),
        ('master', 'Master.'),
        ('baby', 'Baby.'),
        ('babyof', 'Baby Of.')
    ], string='Patient', required=True)
    patient_name = fields.Char(string='Patient', required=True)
    
    day = fields.Char(string='DOB', required=True)
    month = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12')
    ], string='Month', required=True)
    year = fields.Char(string='YEAR', required=True)
    
    age_years = fields.Char(string='Age(years)', required=True)
    age_months = fields.Char(string='Age (Months)', required=True)
    age_days = fields.Char(string='Age (Days)', required=True)
    
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='GENDER', required=True)
    
    weight = fields.Float(string='WEIGHT')
    place = fields.Char(string='PLACE')
    address = fields.Char(string='ADDRESS')
    phone = fields.Char(string='PHONE', size=10)
    blood_group = fields.Selection([
        ('a1', 'A Positive'),
        ('b1', 'B Positive'),
        ('o1', 'O Positive'),
        ('ab1', 'AB Positive'),
        ('a0', 'A Negative'),
        ('b0', 'B Negative'),
        ('o0', 'O Negative'),
        ('ab0', 'AB Negative'),
    ], string='BLOOD GROUP')
    
    referred_by = fields.Char(string='REFERRED BY')
    doc_no = fields.Char(string='REFERRING DOC NO.')
    
    access = fields.Char(string='Access')
    access_used = fields.Char(string='Access Used')
    avf_started_on = fields.Date(string='AVF Started On')
    
    investigations_ids = fields.One2many('patient.investigations', 'patient_id')
    test_ids = fields.One2many('patient.test', 'test_patient_id', string='Test')
    
    patient_master_id = fields.Many2one('patient.master', string='Patient Master', ondelete='restrict')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed')
    ], string='State', default='draft', readonly=True, copy=False)
    

    @api.model
    def create(self, vals):
        if vals.get('reg_type') == 'new':
            patient_master = self.env['patient.master'].create({
                'patient_name': vals.get('patient_name'),
                'patient_type': vals.get('patient_type'),
                'day': vals.get('day'),
                'month': vals.get('month'),
                'year': vals.get('year'),
                'age_years': vals.get('age_years'),
                'age_months': vals.get('age_months'),
                'age_days': vals.get('age_days'),
                'gender': vals.get('gender'),
                'weight': vals.get('weight'),
                'place': vals.get('place'),
                'address': vals.get('address'),
                'phone': vals.get('phone'),
                'blood_group': vals.get('blood_group'),
                'referred_by': vals.get('referred_by'),
                'doc_no': vals.get('doc_no')
            })
            sequence = self.env['ir.sequence'].next_by_code('patient.registration.sequence') or '/'
            reg_no = sequence.zfill(4).upper()

            patient_master.write({'reg_no': reg_no})
            vals['reg_no'] = reg_no
            vals['patient_master_id'] = patient_master.id

        return super(Patient, self).create(vals)
    
    def action_confirm(self):
        print("CONFIRM+_+_+_+_+__+__+__+_+_+_+_+")
        self.ensure_one()
        if self.state != 'confirmed':
            self.state = 'confirmed'

    def action_print(self):
        # Add your code here to handle printing functionality
        pass
      
    @api.onchange('patient_master_id')
    def _onchange_patient_master_id(self):
        if self.reg_type == 'existing' and self.patient_master_id:
            patient_master = self.patient_master_id
            self.reg_no = patient_master.reg_no
            self.patient_name = patient_master.patient_name
            self.patient_type = patient_master.patient_type
            self.day = patient_master.day
            self.month = patient_master.month
            self.year = patient_master.year
            self.age_years = patient_master.age_years
            self.age_months = patient_master.age_months
            self.age_days = patient_master.age_days
            self.gender = patient_master.gender
            self.weight = patient_master.weight
            self.place = patient_master.place
            self.address = patient_master.address
            self.phone = patient_master.phone
            self.blood_group = patient_master.blood_group
            self.referred_by = patient_master.referred_by
            self.doc_no = patient_master.doc_no
    
    @api.onchange('reg_type')
    def _onchange_reg_type(self):
        if self.reg_type == 'new':
            self.reg_no = False
            self.patient_name = False
            self.patient_type = False
            self.day = False
            self.month = False
            self.year = False
            self.age_years = False
            self.age_months = False
            self.age_days = False
            self.gender = False
            self.weight = False
            self.place = False
            self.address = False
            self.phone = False
            self.blood_group = False
            self.referred_by = False
            self.doc_no = False
                
    def write(self, vals):
        result = super(Patient, self).write(vals)
        fields_to_update = [
            'patient_name',
            'patient_type',
            'day',
            'month',
            'year',
            'age_years',
            'age_months',
            'age_days',
            'gender',
            'weight',
            'place',
            'address',
            'phone',
            'blood_group',
            'referred_by',
            'doc_no'
        ]
        patient_master = self.patient_master_id
        fields_vals = {field: vals.get(field) for field in fields_to_update if field in vals}
        if patient_master and fields_vals:
            patient_master.write(fields_vals)
        return result
    
    @api.onchange('day')
    def _check_day_validation(self):
        if self.day:
            try:
                day = int(self.day)
                if day < 1 or day > 31:
                    raise ValidationError("Invalid day. Please enter a valid day between 1 and 31.")
            except ValueError:
                raise ValidationError("Invalid day. Please enter a numeric value for the day.")

    @api.onchange('year')
    def _check_year_validation(self):
        if self.year:
            if not self.year.isdigit():
                raise ValidationError("Invalid year. Please enter a numeric value.")
            year = int(self.year)
            current_year = fields.Date.today().year
            if year < 1900 or year > current_year:
                raise ValidationError(
                    "Invalid year. Please enter a valid year between 1900 and {}.".format(current_year))

    @api.onchange('day', 'month', 'year')
    def _calculate_age(self):
        if self.day and self.month and self.year:
            try:
                birth_date = datetime.strptime('%s-%s-%s' % (self.year, self.month, self.day), '%Y-%m-%d').date()
                today = date.today()
                age = relativedelta(today, birth_date)
                self.age_years = age.years
                self.age_months = age.months
                self.age_days = age.days
            except ValueError:
                pass

    @api.onchange('age_years', 'age_months', 'age_days')
    def _calculate_dob(self):
        if self.age_years or self.age_months or self.age_days:
            try:
                age_years = int(self.age_years) if self.age_years else 0
                age_months = int(self.age_months) if self.age_months else 0
                age_days = int(self.age_days) if self.age_days else 0

                today = date.today()
                dob = today - relativedelta(years=age_years, months=age_months, days=age_days)
                self.day = str(dob.day)
                self.month = str(dob.month)
                self.year = str(dob.year)
            except ValueError:
                pass

    @api.onchange('phone')
    def _check_phone_validation(self):
        if self.phone and not self.phone.isdigit():
            raise ValidationError("Invalid phone number. Please enter only numeric values.")

        if self.phone and len(self.phone) != 10:
            raise ValidationError("Invalid phone number. Please enter a maximum of 10 digits.")
    
            
class Investigations(models.Model):
    _name = "patient.investigations"

    patient_id = fields.Many2one('patient', string='Patient')

    investigation_type = fields.Selection([
        ('ultrasound', 'Ultrasound'),
        ('renal_biopsy', 'Renal Biopsy'),
        ('other', 'Other')
    ], string='Investigation Type', required=True)
    
    date = fields.Date(string='Date')
    report = fields.Text(string='Report')

class Test(models.Model):
    _name = "patient.test"

    test_patient_id = fields.Many2one('patient', string='Test Patient')

    hbs_ag = fields.Date(string='Hbs Ag')
    anti_hbs_ab = fields.Date(string='Anti Hbs Ab')
    anti_hcv = fields.Date(string='Anti HCV')
    hiv_i_ii = fields.Date(string='HIV I & II')
