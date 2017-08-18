from django.db import models

# models hold meta data that is used to describe data held in primary tables


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

