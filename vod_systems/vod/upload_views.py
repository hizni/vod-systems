from django.views.generic import ListView
from django.shortcuts import render, redirect

from models import User_Institution, Institution, Datatype, Transplant_Type, Alias_Identifier, Data_Cleansing_Template, \
    Data_Cleansing_Template_Field, User, Upload_History, Patient_Transplant, Raw_Uploaded_Data
from django.core.files.storage import FileSystemStorage
import datetime
import csv
from django.core.urlresolvers import reverse


class UploadListView(ListView):
    model = Upload_History
    template_name = './vod/user/upload-list.html'

    def get_queryset(self):
        return Upload_History.objects.all()

    def get_context_data(self, **kwargs):
        context = super(UploadListView, self).get_context_data(**kwargs)
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
            myfile = request.FILES['myfile']

            # create file upload audit object and save to database
            uploaded_file = Upload_History(filename=myfile.name, uploaded_by=request.user, upload_date=datetime.datetime.now())
            uploaded_file.save()
            uploaded_file_pk = uploaded_file.id

            # retrieve just created object from database to allow updating of data
            uploaded_file = Upload_History.objects.get(pk=uploaded_file.id)
            # handling a CSV file being uploaded
            if self.validate_file_extension(myfile.name, 'csv'):
                # saving file to server filesystem - do we need to do this??
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                # return render(request, 'core/simple_upload.html', {'uploaded_file_url': uploaded_file_url})

                csv_result, rows_error, total_rows = self.handle_uploaded_file(myfile, uploaded_file_pk , self.account_valid_fields, self.create_account_in_db)

                if csv_result:
                    uploaded_file.outcome = 'CSV read in. Uploaded raw data successful. Rows failed: ' + str(rows_error)
                else:
                    uploaded_file.outcome = 'CSV read in. Raw data upload failed. Rows failed: ' + str(rows_error)

                uploaded_file.rows_errored = rows_error
                uploaded_file.rows_uploaded = total_rows

            else:
                uploaded_file.outcome = 'NON-CSV attempted upload'

            # save file upload audit entry
            uploaded_file.save()

            # return render(request, 'core/simple_upload.html')
        return redirect('upload-list')

    # handles uploaded file
    def handle_uploaded_file(self, uploaded_file, upload_identifier, valid_fields_method, record_creation_function):
        uploaded_file.seek(0)

        # important - csv file must be encoded in UTF-8
        sniffdialect = csv.Sniffer().sniff(uploaded_file.read(10000), delimiters='\t,;')
        uploaded_file.seek(0)

        # print sniffdialect.fieldnames
        data = csv.DictReader(uploaded_file, dialect=sniffdialect)

        if not valid_fields_method(data.fieldnames):
            return False, -1

        result, rows_error, successful_rows = record_creation_function(upload_identifier, data)

        return result, rows_error, successful_rows

    # checks that fields in uploaded CSV file match
    def account_valid_fields(self, field_names):

        # required_fields = ('pk_data', 'fk_pt_institutional_id', 'fk_transplant_day_zero',
        #                    'fk_transplant_start_weight_data_type', 'fk_transplant_start_weight', 'fk_data_type',
        #                    'data_value', 'data_date')

        required_fields = (
            'fk_pt_institutional_id',
            'fk_pt_department_id',
            'fk_pt_identifier_type',
            'fk_pt_identifier_type_value',
            'fk_transplant_number',
            'fk_transplant_type',
            'fk_transplant_day_zero',
            'fk_transplant_start_weight_data_type',
            'fk_transplant_start_weight',
            'fk_transplant_start_renal_function_data_type',
            'fk_transplant_start_renal_function',
            'fk_data_type',
            'data_value',
            'data_date')

        for field in required_fields:
            if field not in field_names:
                return False
        return True

    # create record in database
    def create_account_in_db(self, upload_identifier, dict_data):
        list_data = []
        result = False      # explicity set to false
        rows_error = 0

        # iterate over each row read in from the uploaded file
        for record in dict_data:

            # instantiate
            account = Raw_Uploaded_Data()

            # populate the Raw_Uploaded_Data object
            try:
                account.fk_upload_history_id=upload_identifier
                account.fk_pt_institutional_id=record['fk_pt_institutional_id']
                account.fk_pt_department_id=record['fk_pt_department_id']
                account.fk_pt_identifier_type=record['fk_pt_identifier_type']
                account.fk_pt_identifier_type_value=record['fk_pt_identifier_type_value']
                account.fk_transplant_number=record['fk_transplant_number']
                account.fk_transplant_type=record['fk_transplant_type']
                account.fk_transplant_day_zero=record['fk_transplant_day_zero']
                account.fk_transplant_start_weight_data_type=record['fk_pt_department_id']
                account.fk_transplant_start_weight=record['fk_transplant_start_weight']
                account.fk_transplant_start_renal_function_data_type=record['fk_transplant_start_renal_function_data_type'],
                account.fk_transplant_start_renal_function=record['fk_transplant_start_renal_function']
                account.fk_data_type=record['fk_data_type']
                account.data_value=record['data_value']
                account.data_date=record['data_date']
                account.upload_processing = 'R'

            except Exception:
                account.upload_processing = 'E'
                pass

            # add it to a list of items
            list_data.append(account)

        if list_data:
            # bulk_create will create multiple objects in a single query from the contents of the list_data list
            # created_accounts = Patient_Transplant.objects.bulk_create(list_data)
            created_accounts = Raw_Uploaded_Data.objects.bulk_create(list_data)
            if len(list_data) == len(created_accounts):
                result = True
            else:
                rows_error = len(list_data) - len(created_accounts)

        return result, rows_error, len(created_accounts)

    # validates the extension of a given file
    def validate_file_extension(self, value, extension):
        if value.endswith(extension):
            return True
        return False