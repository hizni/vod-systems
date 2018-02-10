from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect

from models import User_Institution, Institution, Datatype, Transplant_Type, Alias_Identifier, Data_Cleansing_Template, Data_Cleansing_Template_Field, User
from cleansing_forms import DataCleansingTemplateFieldUpdateForm, DataCleansingTemplateCreateForm
from parsley.decorators import parsleyfy

import datetime
import csv

# TODO - implement upload of file to populate data cleansing in form.
# TODO - select form, read in header to get descriptions, and get admin to setup the cleaning properties

# TODO - try to modal above activities


# class DataCleansingTemplateFieldsListView(ListView):
#     model = Data_Cleansing_Template_Field
#     template_name = './common/modal-display-template.html'
#
#     def get_queryset(self):
#         template = Data_Cleansing_Template.objects.get(id=self.kwargs['id'])
#         return Data_Cleansing_Template_Field.objects.all().filter(fk_cleansing_template_id=template)


class DataCleansingTemplateFieldsUpdateView(UpdateView):
    form_class = parsleyfy(DataCleansingTemplateFieldUpdateForm)
    model = Data_Cleansing_Template_Field
    template_name = '../templates/common/modal-template.html'
    view_title = 'Update Data Cleansing Template Field'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(DataCleansingTemplateFieldsUpdateView, self).get_form(form_class)
        form.helper.form_action = reverse('cleansing-template-field-update', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return Data_Cleansing_Template_Field.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('cleansing-profile-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))


class DataCleansingTemplatesListView(ListView):
    model = Data_Cleansing_Template
    template_name = './vod/admin/cleansing-profile-list.html'

    def get_queryset(self):
        # user_insts = User_Institution.objects.values_list('fk_institution_id', flat=True).filter(fk_user_id=self.request.user.id)
        cleansing_templates = Data_Cleansing_Template.objects.all()
        return cleansing_templates

    def get_context_data(self, **kwargs):
        context = super(DataCleansingTemplatesListView, self).get_context_data(**kwargs)
        # context['user_institutions_list'] = User_Institution.objects.all().filter(fk_user_id=self.request.user.id)

        context['users'] = User.objects.all().count()
        context['institutions'] = Institution.objects.all().count()
        context['alias_identifiers'] = Alias_Identifier.objects.all().count()
        context['user_institutions'] = User_Institution.objects.all().filter(fk_user_id=self.request.user.id).count()
        context['datatypes'] = Datatype.objects.all().count()
        context["transplants"] = Transplant_Type.objects.all().count()
        context['cleansing_templates'] = Data_Cleansing_Template.objects.all().count()
        # context['patients'] = Patient.objects.all().filter(fk_institution_id=context["user_institutions"])
        return context

    def post(self, request):
        if request.method == 'POST' and request.FILES['myfile']:

            # submitting file
            myfile = request.FILES['myfile']

            # # create file upload audit object and save to database
            # uploaded_file = Data_Cleansing_Template(
            #     is_active=True,
            #     added_by=request.user,
            #     added_date=datetime.datetime.now())
            # uploaded_file.save()
            # uploaded_file_pk = uploaded_file.id

            # # retrieve just created object from database to allow updating of data
            # uploaded_file = Data_Cleansing_Template.objects.get(pk=uploaded_file.id)
            # # handling a CSV file being uploaded
            if self.validate_file_extension(myfile.name, ['csv']):

                # print 'Handle uploaded file here'
                # separate code fired depending on filetype being handled
                if (myfile.name.endswith('csv')):
                    datafields, data = self.read_csv_file(myfile)

                    template = Data_Cleansing_Template()
                    # if data fields have been returned then create a Data_Cleansing_Template
                    if datafields:
                        template.fk_pt_institutional_id = Institution.objects.get(id=1)
                        template.profile_name = 'foobar'
                        template.is_active = True
                        template.added_by = request.user
                        template.added_date = datetime.datetime.now()
                    # then add the header fields to each Data_Cleansing_Template_Field that belongs to the Template

                        template.save()

                        datafield_objects = []
                        for idx, val in enumerate(datafields):
                            datafield = Data_Cleansing_Template_Field()
                            datafield.fk_cleansing_template_id = template
                            datafield.column_position = idx
                            datafield.description = val
                            datafield.domain_referenced = None
                            datafield.is_nullable = True

                            datafield_objects.append(datafield)

                        Data_Cleansing_Template_Field.objects.bulk_create(datafield_objects)

                else:
                    print 'Unexpected file type attempted upload'

        return redirect('cleansing-profile-list')

    # validates the extension of a given file. checking against a list of possible valid extensions
    def validate_file_extension(self, filename, valid_extension_list):
        for extension in valid_extension_list:
            if filename.endswith(extension):
                return True
        return False

    # handles uploaded file
    def read_csv_file(self, uploaded_file):
        uploaded_file.seek(0)

        # important - csv file must be encoded in UTF-8
        # sniff the dialect of the csv file that will be used in further operations
        sniffdialect = csv.Sniffer().sniff(uploaded_file.read(2048), delimiters='\t,;')

        # read in data from uploaded files
        data = csv.DictReader(uploaded_file, dialect=sniffdialect)

        # fieldnames captures from first row of csv file
        datafields = data.fieldnames

        return datafields, data


class DataCleansingTemplateCreateView(CreateView):
    form_class = parsleyfy(DataCleansingTemplateCreateForm)
    template_name = '../templates/common/modal-template.html'
    view_title = 'Create new cleansing template'

    def form_valid(self, form):
        form.save()
        return redirect('cleansing-profile-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form ,))