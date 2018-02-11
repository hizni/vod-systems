from django.forms import ModelForm
from django import forms
from models import Data_Cleansing_Template, Data_Cleansing_Template_Field, Raw_Uploaded_Data
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Button
from crispy_forms.bootstrap import FormActions
from django.apps import apps
from django.core.urlresolvers import reverse


class DataCleansingTemplateCreateForm(ModelForm):

    class Meta:
        model = Data_Cleansing_Template
        fields = ['fk_pt_institutional_id', 'profile_name']

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()

        self.helper.form_id = 'form'
        self.helper.form_action = reverse('cleansing-profile-create')
        self.helper.form_method = 'post'
        self.helper.form_class = 'generic-modal'
        self.helper.form_show_labels = True
        self.helper.help_text_inline = True
        self.helper.form_show_errors = True
        self.helper.attrs = {'data-validate': 'parsley'}

        super(DataCleansingTemplateCreateForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            # Layout of crispy-forms

            Field('fk_pt_institutional_id',
                  id='inst_id',
                  data_parsley_required='false',
                  data_parsley_length="[0,20]",
                  data_parsley_trigger='change',
                  data_parsley_errors_container="#message-container",
                  data_parsley_required_message='A institution must be entered',
                  ),
            Field('profile_name',
                  id='profile_name',
                  data_parsley_required='false',
                  data_parsley_length="[0,100]",
                  data_parsley_trigger='change',
                  data_parsley_errors_container="#message-container",
                  ),

            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )


class DataCleansingTemplateFieldUpdateForm(ModelForm):

    # get all models
    models = [[' ', '----']]  # initialise with an empty entry
    myapp = apps.get_app_config('vod')
    for model in myapp.models:
        models.append([model, model])

    # get all fields in RawUploadedData model
    fields = [[' ', '----']]
    for field in Raw_Uploaded_Data._meta.fields:
        fields.append(([field.name, field.name]))

    domain_referenced = forms.ChoiceField(label="Choose reference domain", required=False, choices=models)
    data_target_column = forms.ChoiceField(label="Select target field in upload table", required=False, choices=fields)
    class Meta:
        model = Data_Cleansing_Template_Field
        fields = ['column_position', 'description', 'domain_referenced', 'data_target_column', 'is_nullable']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.form_id = 'form'
        self.helper.form_action = ''
        # reverse('cleansing-template-field-update')
        self.helper.form_method = 'post'

        self.helper.form_class = 'generic-modal'
        self.helper.form_show_labels = True
        self.helper.help_text_inline = True
        self.helper.form_show_errors = True
        self.helper.attrs = {'data-validate': 'parsley'}

        super(DataCleansingTemplateFieldUpdateForm, self).__init__(*args, **kwargs)

        # gets the all available institutions for this user
        # myapp = apps.get_app_config('vod')
        #myapp = ['aaaa', 'vvvv', 'dsdfdf']
        #self.fields['domains'].choices = myapp

        self.helper.layout = Layout(
            Field('column_position',
                  id='column_position',
                  #data_parsley_required='false',
                  #disabled='true',
                  data_parsley_length="[0,100]",
                  data_parsley_trigger='change',
                  data_parsley_errors_container="#message-container",
                  #data_parsley_required_message='A column position must be entered',
                  ),
            Field('description',
                  id='description',
                  #data_parsley_required='false',
                  data_parsley_length="[0,255]",
                  data_parsley_trigger='change',
                  data_parsley_errors_container="#message-container",
                  #data_parsley_required_message='A column position must be entered',
                  ),
            Field('domain_referenced',
                  id='domain_referenced',
                  #data_parsley_required='false',
                  data_parsley_length="[0,255]",
                  data_parsley_trigger='change',
                  data_parsley_errors_container="#message-container",
                  # data_parsley_required_message='',
                  ),
            Field('data_target_column',
                  id='data_target_column',
                  # data_parsley_required='false',
                  data_parsley_length="[0,255]",
                  data_parsley_trigger='change',
                  data_parsley_errors_container="#message-container",
                  # data_parsley_required_message='',
                  ),
            Field('is_nullable',
                  id='is_nullable',
                  #data_parsley_required='false',
                  data_parsley_trigger='change',
                  data_parsley_errors_container="#message-container",
                  #data_parsley_required_message='null must be set',
                  ),
            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )

