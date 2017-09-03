from crispy_forms.bootstrap import PrependedText
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class SimpleForm(ModelForm):
    # helper = FormHelper()
    # helper.form_tag = False

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password', 'is_staff', 'is_superuser']
        # fields = ['username', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(SimpleForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'form'
        self.helper.form_action = '.'
        self.helper.form_class = 'generic-modal'
        self.helper.attrs = {'data-validate-parsley': 'parsley'}
        self.helper.layout = Layout(
            Field('username',  id="username", required=True, form_class="has_warning"),
            Field('password', id="password", required=True),
            Field('confirm_password', id="confirm_password", required=True, data_parsley_equalto="#password"),
        )
        # self.helper.add_input(Submit('submit', 'Submit'))











