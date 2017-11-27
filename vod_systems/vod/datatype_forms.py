from django.forms import ModelForm
from models import Datatype
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Button
from crispy_forms.bootstrap import FormActions
from django.core.urlresolvers import reverse


class DatatypeCreateUpdateForm(ModelForm):

    class Meta:
        model = Datatype
        fields = ['code', 'description', 'unit']

    def __init__(self, *args, **kwargs):
        super(DatatypeCreateUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_id = 'form'
        self.helper.form_action = reverse('datatype-create')
        self.helper.form_method = 'post'
        self.helper.form_class = 'generic-modal'
        self.helper.form_show_labels = True
        self.helper.help_text_inline = True
        self.helper.form_show_errors = True
        self.helper.attrs = {'data-validate': 'parsley'}
        self.helper.layout = Layout(
            # Layout of crispy-forms

            HTML('Enter details for a datatype'),
            Field('code',
                  id='code',
                  data_parsley_required='true',
                  data_parsley_length="[0,100]",
                  data_parsley_trigger='change',
                  data_parsley_errors_container="#message-container",
                  data_parsley_required_message='A code must be entered',
                  ),
            Field('description',
                  id='description',
                  data_parsley_required='false',
                  data_parsley_length="[0,255]",
                  data_parsley_trigger='change',
                  data_parsley_errors_container="#message-container",
                  ),
            Field('unit',
                  id='unit',
                  data_parsley_required='false',
                  data_parsley_length="[0,20]",
                  data_parsley_trigger='change',
                  data_parsley_errors_container="#message-container",
                  ),
            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )


class DatatypeRetireForm(ModelForm):

    class Meta:
        model = Datatype
        fields = ['is_active']

    def __init__(self, *args, **kwargs):
        super(DatatypeRetireForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'form'
        self.helper.form_method = 'post'
        self.helper.form_action = ""

        self.helper.form_show_labels = True
        self.helper.help_text_inline = True
        self.helper.form_show_errors = True
        self.helper.attrs = {'data-validate': 'parsley'}

        self.helper.layout = Layout(

            HTML("Currently {{object.description}} has the following activity status: "),
            Field('is_active',
                  id='is_active'
                  ),

            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary align-right"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )