from django.db import models


GENDER_CHOICES = (
    ('Male', 'M'),
    ('Female', 'F'),
    ('Indeterminate', 'I'),
    ('Unknown', 'U'),
)

# metadata - models hold meta data that is used to describe data held in primary tables

class Institution(models.Model):
    code = models.CharField(max_length=20)  #institution code
    description = models.CharField(max_length=100)


class AliasIdentifier(models.Model):
    code = models.CharField(max_length=20) # identifier type
    description = models.CharField(max_length=100)


class DataType(models.Model):
    code = models.CharField(max_length=20)  # units
    description = models.CharField(max_length=255)


class TransplantType(models.Model):
    code = models.CharField(max_length=20) # transplant type
    description = models.CharField(max_length=100)


# primary data

class Patient(models.Model):
    surname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateTimeField()
    date_of_death = models.DateTimeField(blank=True, null=True)


class PatientIdentifier(models.Model):
    fk_patient_id = models.ForeignKey(Patient)
    fk_institution_id = models.ForeignKey(Institution)
    department_id = models.CharField(max_length=100)
    fk_identifier_type = models.ForeignKey(AliasIdentifier)
    pt_identifier_type_value = models.CharField(max_length=50)


class Transplant(models.Model):
    fk_patient_id = models.ForeignKey(Patient)
    number = models.IntegerField()
    fk_transplant_type = models.ForeignKey(TransplantType)
    day_zero = models.DateField()
    start_weight = models.FloatField()
    start_renal_function = models.FloatField()



