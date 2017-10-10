from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
    ('I', 'Indeterminate'),
    ('U', 'Unknown'),
)

# metadata - models hold meta data that is used to describe data held in primary tables


class Institution(models.Model):
    code = models.CharField(max_length=20)  # institution code
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class Alias_Identifier(models.Model):
    code = models.CharField(max_length=20) # identifier type
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class Datatype(models.Model):
    code = models.CharField(max_length=20)  # units
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


class Transplant_Type(models.Model):
    code = models.CharField(max_length=20)  # transplant type
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

# secondary


class User_Institution(models.Model):
    fk_user_id = models.ForeignKey(User, related_name='institution_belongs_to')
    fk_institution_id = models.ForeignKey(Institution)

# primary data


class Patient(models.Model):
    surname = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateTimeField()
    date_of_death = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Patient_Identifier(models.Model):
    fk_patient_id = models.ForeignKey(Patient)
    fk_institution_id = models.ForeignKey(Institution)
    department_id = models.CharField(max_length=100)
    fk_identifier_type = models.ForeignKey(Alias_Identifier)
    pt_identifier_type_value = models.CharField(max_length=50)


class Transplant(models.Model):
    fk_patient_id = models.ForeignKey(Patient)
    number = models.IntegerField()
    fk_transplant_type = models.ForeignKey(Transplant_Type)
    day_zero = models.DateTimeField()
    start_weight = models.FloatField()
    start_renal_function = models.FloatField()


class Upload_History(models.Model):
    filename = models.CharField(max_length=255)
    outcome = models.CharField(max_length=255)
    upload_date = models.DateTimeField()
    uploaded_by = models.CharField(max_length=255)



