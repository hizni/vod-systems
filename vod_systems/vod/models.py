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
    code = models.CharField(max_length=100)  # units
    description = models.CharField(max_length=255)
    unit = models.CharField(max_length=20)
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
    fk_institution_id = models.ForeignKey(Institution)
    is_active = models.BooleanField(default=True)


class Patient_Identifier(models.Model):
    fk_patient_id = models.ForeignKey(Patient)
    department_id = models.CharField(max_length=100)
    fk_identifier_type = models.ForeignKey(Alias_Identifier)
    pt_identifier_type_value = models.CharField(max_length=50)


class Patient_Transplant(models.Model):
    fk_patient_id = models.ForeignKey(Patient)
    number = models.IntegerField()
    fk_transplant_type = models.ForeignKey(Transplant_Type)
    day_zero = models.DateTimeField()
    start_weight = models.FloatField()
    start_renal_function = models.FloatField()


class Upload_History(models.Model):
    filename = models.CharField(max_length=255)
    outcome = models.CharField(max_length=255)
    rows_uploaded  = models.IntegerField(default=0)
    row_cleaned = models.IntegerField(default=0)
    rows_errored = models.IntegerField(default=0)
    upload_date = models.DateTimeField(default=0)
    uploaded_by = models.CharField(max_length=255)


class Clean_Uploaded_Data(models.Model):
    fk_batch_id = models.ForeignKey(Upload_History)
    fk_patient = models.ForeignKey(Patient_Identifier)
    fk_transplant = models.ForeignKey(Patient_Transplant)
    fk_datatype = models.ForeignKey(Datatype)
    value = models.FloatField()
    date_occurred = models.DateTimeField()


class Raw_Uploaded_Data(models.Model):
    R = 'R'
    C = 'C'
    E = 'E'
    N = 'N'
    UPLOAD_PROCESSING = (
        (R, 'Raw'),
        (C, 'Cleaned'),
        (E, 'Errored'),
        (N, 'Null'),
    )

    fk_upload_history = models.ForeignKey(Upload_History)
    fk_pt_institutional_id = models.CharField(max_length=100)
    fk_pt_department_id = models.CharField(max_length=100)
    fk_pt_identifier_type = models.CharField(max_length=50)
    fk_pt_identifier_type_value = models.CharField(max_length=50)
    fk_transplant_number = models.IntegerField()
    fk_transplant_type = models.CharField(max_length=100)
    fk_transplant_day_zero = models.DateTimeField()
    fk_transplant_start_weight_data_type= models.CharField(max_length=100)
    fk_transplant_start_weight = models.FloatField()
    fk_transplant_start_renal_function_data_type = models.CharField(max_length=100)
    fk_transplant_start_renal_function = models.FloatField()
    fk_data_type = models.CharField(max_length=100)
    data_value = models.FloatField()
    data_date = models.DateTimeField()
    upload_processing = models.CharField(max_length=10, choices=UPLOAD_PROCESSING)





