
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from models import Patient, Institution, AliasIdentifier, DataType, TransplantType


class InstitutionForm(ModelForm):
    class Meta:
        model = Institution
        fields = ['code', 'description']


class AliasIdentifierForm(ModelForm):
    class Meta:
        model = AliasIdentifier
        fields = ['code', 'description']


class DataTypeForm(ModelForm):
    class Meta:
        model = DataType
        fields = ['code', 'description']


class TransplantTypeForm(ModelForm):
    class Meta:
        model = TransplantType
        fields = ['code', 'description']


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['surname', 'firstname', 'gender', 'date_of_birth', 'date_of_death']


# Extending the default Django UserCreationForm that just has the following fields:
#   username, password
class ExtendedUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="First name", min_length=5, max_length=15)
    last_name = forms.CharField(label="Last name")
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(ExtendedUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user

