from django.forms import ModelForm
from django import forms
from models import Patient,Patient_Identifier, Patient_Transplant
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Button, Div
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from django.core.urlresolvers import reverse
from bootstrap3_datetime.widgets import DateTimePicker


class PatientAliasCreateForm(ModelForm):
    department_id = forms.Field(required=False)

    class Meta:
        model = Patient_Identifier
        fields = ['department_id', 'fk_patient_id', 'fk_identifier_type', 'pt_identifier_type_value']

    def __init__(self, *args, **kwargs):
        self.pid = kwargs.pop('pid', None)
        super(PatientAliasCreateForm, self).__init__(*args, **kwargs)

        self.fields['fk_identifier_type'].label_from_instance = lambda obj: "%s" % obj.description

        self.helper = FormHelper()

        self.helper.form_id = 'form'
        self.helper.form_action = reverse('patient-create-alias', args=[self.pid])
        self.helper.form_method = 'post'
        self.helper.form_class = 'generic-modal'
        self.helper.form_show_labels = True
        self.helper.help_text_inline = True
        self.helper.form_show_errors = True
        self.helper.attrs = {'data-validate': 'parsley'}

        self.helper.layout = Layout(
            Field('department_id',
                  id='department_id',
                  ),
            Field('fk_identifier_type',
                  id='fk_identifier_type',
                  ),
            Field('pt_identifier_type_value',
                  id='pt_identifier_type_value',
                  ),
            Field('fk_patient_id', id='fk_patient_id', type='hidden', label=''),
            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )


class PatientTransplantCreateForm(ModelForm):

    class Meta:
        model = Patient_Transplant
        fields = ['number', 'fk_patient_id', 'fk_transplant_type','day_zero','start_weight','start_renal_function']

    def __init__(self, *args, **kwargs):
        self.pid = kwargs.pop('pid', None)

        super(PatientTransplantCreateForm, self).__init__(*args, **kwargs)

        self.fields['fk_transplant_type'].label_from_instance = lambda obj: "%s" % obj.description
        self.helper = FormHelper()

        self.helper.form_id = 'form'
        self.helper.form_action = reverse('patient-create-transplant', args=[self.pid])
        self.helper.form_method = 'post'
        self.helper.form_class = 'generic-modal'
        self.helper.form_show_labels = True
        self.helper.help_text_inline = True
        self.helper.form_show_errors = True
        self.helper.attrs = {'data-validate': 'parsley'}

        self.helper.layout = Layout(
            Field('number',
                  id='number',
                  ),
            Field('fk_transplant_type',
                  id='fk_transplant_type',
                  ),
            Field('day_zero',
                  id='day_zero',
                  ),
            Field('start_weight',
                  id='start_weight',
                  ),
            Field('start_renal_function',
                  id='start_renal_function',
                  ),
            Field('fk_patient_id', id='fk_patient_id', type='hidden', label=''),
            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )


class PatientCreateUpdateForm(ModelForm):

    # checkboxselectmultiple = forms.Field()

    class Meta:
        model = Patient
        # fields = ['surname', "first_name", 'gender', 'date_of_birth', 'date_of_death', 'fk_institution_id']
        fields = ['surname', 'first_name', 'gender', 'date_of_birth', 'fk_institution_id']

    def __init__(self, *args, **kwargs):
        super(PatientCreateUpdateForm, self).__init__(*args, **kwargs)

        self.fields['fk_institution_id'].label_from_instance = lambda obj: "%s" % obj.description
        # self.fields['checkboxselectmultiple'].choices = ((x.fk_identifier_type.code, x.pt_identifier_type_value) for x in Patient_Identifier.objects.all())

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
                    HTML('Please enter some details for a patient'),
                    Field('surname',
                          id='surname',
                          data_parsley_length="[0,255]",
                          data_parsley_trigger='change',
                          data_parsley_errors_container="#message-container",
                          ),
                    Field('first_name',
                          id='first_name',
                          data_parsley_length="[0,255]",
                          data_parsley_trigger='change',
                          data_parsley_errors_container="#message-container",
                          ),
                    Field('gender',
                          id='gender'
                          ),
                    Field('date_of_birth',
                          id='date_of_birth'
                          ),
                ),
                Tab(
                    'Institution Details',
                    HTML('Select the institution(s) this patient belongs to: '),
                    Field('fk_institution_id', id='fk_institution_id', label=''),
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

            HTML("Currently {{object.firstname}} {{object.surname}} has the following activity status: "),
            Field('is_active',
                  id='is_active'
                  ),

            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary align-right"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )