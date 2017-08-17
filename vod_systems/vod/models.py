from django.db import models


class Institution(models.Model):
    institution_code = models.CharField(max_length=20)
    description = models.CharField(max_length=100)


class AliasIdentifier(models.Model):
    identifier_type = models.CharField(max_length=20)
    description = models.CharField(max_length=100)


class DataType(models.Model):
    units = models.CharField(max_length=20)
    description = models.CharField(max_length=255)


class TransplantType(models.Model):
    description = models.CharField(max_length=100)

