from django.forms import ModelForm
from models import Data_Cleansing_Template
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Button
from crispy_forms.bootstrap import FormActions
from django.core.urlresolvers import reverse


class DataCleansingTemplateCreateView(ModelForm):

    class Meta:
        model = Data_Cleansing_Template
        fields = ['fk_pt_institutional_id', 'profile_name']

    def __init__(self, *args, **kwargs):
        super(DataCleansingTemplateCreateView, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_id = 'form'
        self.helper.form_action = reverse('cleansing-profile-create')
        self.helper.form_method = 'post'
        self.helper.form_class = 'generic-modal'
        self.helper.form_show_labels = True
        self.helper.help_text_inline = True
        self.helper.form_show_errors = True
        self.helper.attrs = {'data-validate': 'parsley'}
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