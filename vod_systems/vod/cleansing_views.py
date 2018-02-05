from django.views.generic import ListView, CreateView
from django.shortcuts import render, redirect

from models import Data_Cleansing_Template_Field, Data_Cleansing_Template, User_Institution, Institution
from cleansing_forms import DataCleansingTemplateCreateView
from parsley.decorators import parsleyfy

import datetime
import csv

# TODO - implement upload of file to populate data cleansing in form.
# TODO - select form, read in header to get descriptions, and get admin to setup the cleaning properties

# TODO - try to modal above activities


class DataCleansingTemplatesListView(ListView):
    model = Data_Cleansing_Template
    template_name = './vod/admin/cleansing-profile-list.html'

    def get_queryset(self):
        # user_insts = User_Institution.objects.values_list('fk_institution_id', flat=True).filter(fk_user_id=self.request.user.id)
        cleansing_templates = Data_Cleansing_Template.objects.all()
        return cleansing_templates

    def get_context_data(self, **kwargs):
        context = super(DataCleansingTemplatesListView, self).get_context_data(**kwargs)
        context['user_institutions_list'] = User_Institution.objects.all().filter(fk_user_id=self.request.user.id)
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

                print 'Handle uploaded file here'
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

                    # for record in data:
                    #     for field in datafields:
                    #         print(record[field])


                #     # saving file to server filesystem - do we need to do this??
                #     fs = FileSystemStorage()
                #     filename = fs.save(myfile.name, myfile)

                #     uploaded_file_url = fs.url(filename)
                #     # return render(request, 'core/simple_upload.html', {'uploaded_file_url': uploaded_file_url})
                #
                #     csv_result, rows_error, total_rows = self.handle_uploaded_file(myfile, uploaded_file_pk , self.account_valid_fields, self.create_account_in_db)
                #
                #     if csv_result:
                #         uploaded_file.outcome = 'CSV read in. Uploaded raw data successful. Rows failed: ' + str(rows_error)
                #     else:
                #         uploaded_file.outcome = 'CSV read in. Raw data upload failed. Rows failed: ' + str(rows_error)
                #
                #     uploaded_file.rows_errored = rows_error
                #     uploaded_file.rows_uploaded = total_rows
                #
            else:
                 print 'Unexpected file type attempted upload'
            #
            # # save file upload audit entry
            # uploaded_file.save()
            #
            # # return render(request, 'core/simple_upload.html')
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
    form_class = parsleyfy(DataCleansingTemplateCreateView)
    template_name = '../templates/common/modal-template.html'
    view_title = 'Create new cleansing template'

    def form_valid(self, form):
        form.save()
        return redirect('cleansing-profile-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form ,))