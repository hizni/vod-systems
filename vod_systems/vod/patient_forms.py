from django.forms import ModelForm
from django import forms
from models import Patient, User_Institution
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Button
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from django.core.urlresolvers import reverse
from bootstrap3_datetime.widgets import DateTimePicker


class PatientCreateUpdateForm(ModelForm):

    date_of_birth = forms.DateTimeField(required = False,
                                        widget = DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                          "pickTime": False
                                                                         }))

    date_of_death = forms.DateTimeField(required=False,
                                        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                                                       "pickSeconds": False
                                                                       }))
    # institutions = forms.ModelChoiceField(required=True, queryset=User_Institution.objects.all())

    class Meta:
        model = Patient
        fields = ['surname', "first_name", 'gender', 'date_of_birth', 'date_of_death', 'fk_institution_id']

    def __init__(self, *args, **kwargs):
        super(PatientCreateUpdateForm, self).__init__(*args, **kwargs)

        # self.fields['institutions'].choices = ((x.code, x.description) for x in User_Institution.objects.all().filter(fk_user_id=self.instance.id))
        self.helper = FormHelper()

        self.helper.form_id = 'form'
        self.helper.form_action = reverse('patient-create')
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
            TabHolder(
                Tab(
                    'Patient Details',
                    Field('surname',
                          id='surname',
                          data_parsley_length="[0,255]",
                          data_parsley_trigger='change'),
                    Field('first_name',
                          id='first_name',
                          data_parsley_length="[0,255]",
                          data_parsley_trigger='change'
                          ),
                    Field('gender',
                          id='gender',
                          data_parsley_length="[0,10]",
                          data_parsley_trigger='change'
                          ),
                    Field('date_of_birth',
                          id='date_of_birth'
                          ),
                    Field('date_of_death',
                          id='date_of_death'
                          ),
                ),
                Tab(
                    'Institution Details',
                    Field('fk_institution_id', id='fk_institution_id'),
                )
            ),
            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )


class PatientRetireForm(ModelForm):

    class Meta:
        model = Patient
        fields = ['is_active']

    def __init__(self, *args, **kwargs):
        super(PatientRetireForm, self).__init__(*args, **kwargs)

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

            HTML("Currently {{object.firstname}} {{object.surname}} has the following activity status: "),
            Field('is_active',
                  id='is_active'
                  ),

            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary align-right"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )