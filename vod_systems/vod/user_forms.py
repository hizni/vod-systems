from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from models import Institution, User_Institution
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Button, ButtonHolder
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from django.core.urlresolvers import reverse


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login', 'Login', css_class='btn-primary')
            )
        )


class UserCreateForm(ModelForm):
    # helper = FormHelper()
    # helper.form_tag = False

    # setting up properties of html components to do with the field and associated components
    # but the error text message does seem to get set here..... html5 error message?
    username = forms.CharField(help_text='')
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput,
                                       label='Password Check',
                                       help_text='Re-enter the password..')
    checkboxselectmultiple = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'style': 'overflow : scroll; height:200'}),
        label='Institutions',
        required=True)
    is_staff = forms.BooleanField(label='Staff')
    is_superuser = forms.BooleanField(label='Administrator')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password', 'is_staff',
                  'is_superuser']

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        # self.fields['staff_roles'].choices=[('1', 'Standard user'), ('2', 'Administrator')]

        self.fields['checkboxselectmultiple'].choices = ((x.code, x.description) for x in Institution.objects.all())

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
            # Div(id='message-container', css_class='validation-errors-container'),
            TabHolder(
                Tab('User Details',
                    HTML('Please add some details about the user'),
                    Field('first_name',
                          id='first_name'
                          ),
                    Field('last_name',
                          id='last_name'
                          ),
                    Field('email',
                          id='email',
                          data_parsley_trigger='change',
                          data_parsley_errors_container="#message-container",
                          data_parsley_error_message='The e-mail address entered is not valid',
                          ),
                    Field('username',
                          id='username',
                          required=True,
                          autocomplete='off',
                          data_parsley_errors_container="#message-container",
                          data_parsley_required_message='Please enter a username',
                          ),
                    Field('password',
                          id='password',
                          data_parsley_errors_container="#message-container",
                          data_parsley_required_message='A password must be entered',
                          required=True
                          ),
                    Field('confirm_password',
                          id="confirm_password",
                          required=True,
                          label="Password check:",
                          data_parsley_equalto="#password",
                          data_parsley_trigger='change',
                          data_parsley_errors_container="#message-container",
                          data_parsley_required_message='Re-confirm the password',
                          data_parsley_error_message='Make sure that the password matches'
                          ),
                    ),
                Tab('Roles',
                    HTML('Please select a role for the user'),
                    Field('is_staff',
                          id='is_staff',
                          required=True,
                          help_text='',
                          data_parsley_errors_container="#message-container",
                          data_parsley_required_message='A role must be selected for the user',
                          data_parsley_multiple="user_roles",
                          ),
                    Field('is_superuser',
                          id='is_superuser',
                          help_text='',
                          data_parsley_errors_container="#message-container",
                          data_parsley_required_message='A role must be selected for the user',
                          data_parsley_multiple="user_roles",
                          ),
                    ),
                Tab(
                    'Institutions',
                    HTML('Please select the institutions the user belongs to'),
                    Field('checkboxselectmultiple',
                          style="background: #FFFFFF; padding: 10px;",
                          required=False,
                          data_parsley_errors_container="#message-container",
                          data_parsley_required_message='An institution must be selected',
                          data_parsley_mincheck_message='At least %s institution must be selected',
                          data_parsley_mincheck="1"
                          ),
                ),
            ),

            FormActions(

                Submit('save_changes', 'Save changes', css_class="btn-primary"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )


class UserDetailUpdateForm(ModelForm):
    # helper = FormHelper()
    # helper.form_tag = False

    # setting up properties of html components to do with the field and associated components
    # but the error text message does seem to get set here..... html5 error message?
    username = forms.CharField(help_text='')
    checkboxselectmultiple = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(
        attrs={'style': 'overflow : scroll; height:200'}),
        label='')

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

        super(UserDetailUpdateForm, self).__init__(*args, **kwargs)

        # get empty list of institutions
        insts = Institution.objects.all()
        user_chosen_inst = User_Institution.objects.values_list('fk_institution_id', flat=True).filter(
            fk_user_id=self.instance.id)

        # gets the avaialble institutions
        self.fields['checkboxselectmultiple'].choices = ((x.id, x.description) for x in insts)
        # ticks the chosen institutions for this user
        self.fields['checkboxselectmultiple'].initial = list(user_chosen_inst)

        self.helper.layout = Layout(
            # Layout of crispy-forms
            # Default: required = false
            # Other validation criteria then get applied if data is filled in.
            # See parsleyjs documentation: http://parsleyjs.org/doc/
            #   data_parsley_length="[minimum-value,maximum-value]"

            TabHolder(
                Tab(
                    'User Details',
                    Field('first_name',
                          id='first_name'
                          # data_parsley_length="[5,10]",
                          # data_parsley_trigger='change'
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
                ),
                Tab(
                    'User Roles',
                    Field('is_staff',
                          id='is_staff'
                          ),
                    Field('is_superuser',
                          id='is_superuser'
                          ),
                ),
                Tab(
                    'User Institutions',
                    Field('checkboxselectmultiple',
                          id='user_insts',
                          error_message="At least one Institution must be chosen",
                          data_parsley_required="true",
                          data_parsley_trigger="click",
                          data_parsley_mincheck="1"),
                )
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
