from django.forms import ModelForm
from django import forms
from models import Institution
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Button
from crispy_forms.bootstrap import FormActions
from django.core.urlresolvers import reverse


class InstitutionCreateUpdateForm(ModelForm):

    class Meta:
        model = Institution
        fields = ['code', 'description']

    def __init__(self, *args, **kwargs):
        super(InstitutionCreateUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_id = 'form'
        self.helper.form_action = reverse('institution-create')
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

            Field('code',
                  id='code',
                  required=True,
                  data_parsley_length="[0,20]",
                  data_parsley_trigger='change'
                  ),
            Field('description',
                  id='description',
                  data_parsley_length="[0,100]",
                  data_parsley_trigger='change'
                  ),

            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )


class InstitutionRetireForm(ModelForm):

    class Meta:
        model = Institution
        fields = ['is_active']

    def __init__(self, *args, **kwargs):
        super(InstitutionRetireForm, self).__init__(*args, **kwargs)

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

            HTML("Currently {{object.description}} has the following activity status: "),
            Field('is_active',
                  id='is_active'
                  ),

            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary align-right"),
                Button('cancel', "Cancel", css_class='btn', onclick="$('#modal').modal('hide');"),
            )
        )