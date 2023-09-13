from odoo import models, fields, api
from datetime import date, datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class PatientMaster(models.Model):
    _name = 'patient.master'
    _description = 'Patient Details form and Kanban'
    #Registration Number
    reg_no = fields.Char(string='Register Number', readonly=True)
    #Patient Details    
    patient_type = fields.Selection([
        ('mr', 'Mr.'),
        ('mrs', 'Mrs.'),
        ('ms', 'Ms.'),
        ('newborn', 'New Born.'),
        ('master', 'Master.'),
        ('baby', 'Baby.'),
        ('babyof', 'Baby Of.')
    ],required=True)
    patient_name = fields.Char(string='Patient Name', required=True)
    # Date Of Birth
    day = fields.Char(string='Day', required=True)
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
    # AGE
    age_years = fields.Char(string='AGE', required=True)
    age_months = fields.Char(string='Age (Months)', required=True)
    age_days = fields.Char(string='Age (Days)', required=True)
    #Other Details
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
    ], string='Blood_group')
    referred_by = fields.Char(string='Refered_by')
    doc_no = fields.Char(string='Ref_doc_no')
    #photo
    image_patient = fields.Binary(string='Patient Image')
#----------------------------------------------------------------------------------------------------------------
    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('patient.registration.sequence') or '/'
        vals['reg_no'] = sequence.zfill(4).upper()
        return super(PatientMaster, self).create(vals)

    def write(self, vals):
        if 'reg_no' not in vals:
            sequence = self.env['ir.sequence'].next_by_code('patient.registration.sequence') or '/'
            vals['reg_no'] = sequence.zfill(4).upper()
        return super(PatientMaster, self).write(vals)

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

    @api.onchange('phone')
    def _check_phone_validation(self):
        if self.phone and not self.phone.isdigit():
            raise ValidationError("Invalid phone number. Please enter only numeric values.")

        if self.phone and len(self.phone) != 10:
            raise ValidationError("Invalid phone number. Please enter a maximum of 10 digits.")    
        
    def name_get(self):
        result = []
        for record in self:
            name = record.patient_name
            result.append((record.id, name))
        return result
#--------------------------------------------------------------------------------------------------------------------
