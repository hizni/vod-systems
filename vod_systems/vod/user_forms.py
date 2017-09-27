from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Button
from crispy_forms.bootstrap import FormActions
from django.core.urlresolvers import reverse


class UserCreateForm(ModelForm):
    # helper = FormHelper()
    # helper.form_tag = False

    # setting up properties of html components to do with the field and associated components
    # but the error text message does seem to get set here..... html5 error message?
    username = forms.CharField(help_text='')
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Password Check', help_text='Re-enter the password..')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password', 'is_staff', 'is_superuser']

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_id = 'form'
        self.helper.form_action = reverse('user-create')
        self.helper.form_method = 'post'
        self.helper.form_class = 'generic-modal'
        self.helper.form_show_labels = True
        self.helper.help_text_inline = True
        self.helper.form_show_errors = True
        self.helper.attrs = {'data-validate': 'parsley'}
        self.helper.layout = Layout(
            # Layout of crispy-forms
            # Default: required = false
            # Other validation criteria then get applied if data is filled in.
            # See parsleyjs documentation: http://parsleyjs.org/doc/
            #   data_parsley_length="[minimum-value,maximum-value]"

            Field('first_name',
                  id='first_name',
                  data_parsley_length="[5,10]",
                  data_parsley_trigger='change'
                  ),
            Field('last_name',
                  id='last_name'
                  ),
            Field('email',
                  id='email',
                  data_parsley_trigger='change'
                  ),
            Field('username',
                  id='username',
                  required=True,
                  autocomplete='off'
                  ),
            Field('password',
                  id='password',
                  required=True
                  ),
            Field('confirm_password',
                  id="confirm_password",
                  required=True,
                  label="Password check:",
                  data_parsley_equalto="#password",
                  data_parsley_trigger='change',

                  error_message="The passwords do not match."),

            Field('is_staff',
                  id='is_staff'
                  ),
            Field('is_superuser',
                  id='is_superuser'
                  ),

            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )


class UserRetireForm(ModelForm):

    class Meta:
        model = User
        fields = ['is_active']

    def __init__(self, *args, **kwargs):
        super(UserRetireForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'form'
        self.helper.form_method = 'post'
        self.helper.form_action = ""

        self.helper.form_show_labels = True
        self.helper.help_text_inline = True
        self.helper.form_show_errors = True
        self.helper.attrs = {'data-validate': 'parsley'}

        self.helper.layout = Layout(
            # Layout of crispy-forms
            # Default: required = false
            # Other validation criteria then get applied if data is filled in.
            # See parsleyjs documentation: http://parsleyjs.org/doc/
            #   data_parsley_length="[minimum-value,maximum-value]"

            HTML("Currently {{object.first_name}} {{object.last_name}} has the following activity status: "),
            Field('is_active',
                  id='is_active'
                  ),

            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary align-right"),
                # Submit('cancel', 'Cancel'),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )


class UserUpdateForm(ModelForm):
    # helper = FormHelper()
    # helper.form_tag = False

    # setting up properties of html components to do with the field and associated components
    # but the error text message does seem to get set here..... html5 error message?
    username = forms.CharField(help_text='')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'is_staff', 'is_superuser']
        # fields = ['username', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_id = 'form'
        self.helper.form_method = 'post'
        self.helper.form_action = ""

        self.helper.form_show_labels = True
        self.helper.help_text_inline = True
        self.helper.form_show_errors = True
        self.helper.attrs = {'data-validate': 'parsley'}

        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            # Layout of crispy-forms
            # Default: required = false
            # Other validation criteria then get applied if data is filled in.
            # See parsleyjs documentation: http://parsleyjs.org/doc/
            #   data_parsley_length="[minimum-value,maximum-value]"

            Field('first_name',
                  id='first_name',
                  data_parsley_length="[5,10]",
                  data_parsley_trigger='change'
                  ),
            Field('last_name',
                  id='last_name'
                  ),
            Field('email',
                  id='email',
                  data_parsley_trigger='change'
                  ),
            Field('username',
                  id='username',
                  required=True,
                  autocomplete='off'
                  ),

            Field('is_staff',
                  id='is_staff'
                  ),
            Field('is_superuser',
                  id='is_superuser'
                  ),

            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )











