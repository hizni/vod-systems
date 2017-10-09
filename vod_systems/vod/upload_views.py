from django.views.generic import ListView
from django.shortcuts import render, redirect

from models import UploadHistory, Transplant
from django.core.files.storage import FileSystemStorage
import datetime
import csv
from django.core.urlresolvers import reverse


class UploadListView(ListView):
    model = UploadHistory
    template_name = './vod/user/upload-list.html'

    def get_queryset(self):
        return UploadHistory.objects.all()

    def post(self, request):
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']

            # create file upload audit
            uploaded_file = UploadHistory(filename=myfile.name, uploaded_by=request.user, upload_date=datetime.datetime.now())

            if self.validate_file_extension(myfile.name, 'csv'):
                # saving file to server filesystem - do we need to do this??
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                # return render(request, 'core/simple_upload.html', {'uploaded_file_url': uploaded_file_url})

                csv_result, rows_error = self.handle_uploaded_file(myfile, self.account_valid_fields, self.create_account_in_db)

                if csv_result:
                    uploaded_file.outcome = 'CSV uploaded. Database upload successful. Rows failed: ' + rows_error
                else:
                    uploaded_file.outcome = 'CSV uploaded. Database load failed. Rows failed: ' + rows_error

            else:
                uploaded_file.outcome = 'NON-CSV attempted upload'

            # save file upload audit entry
            uploaded_file.save()

            # return render(request, 'core/simple_upload.html')
        return redirect('upload-list')

    # handles uploaded file
    def handle_uploaded_file(self, uploaded_file, valid_fields_method, record_creation_function):
        uploaded_file.seek(0)

        # important - csv file must be encoded in UTF-8
        sniffdialect = csv.Sniffer().sniff(uploaded_file.read(10000), delimiters='\t,;')
        uploaded_file.seek(0)

        # print sniffdialect.fieldnames
        data = csv.DictReader(uploaded_file, dialect=sniffdialect)

        if not valid_fields_method(data.fieldnames):
            return False, -1

        result, rows_error = record_creation_function(data)

        return result, rows_error

    # checks that fields in uploaded CSV file match
    def account_valid_fields(self, field_names):

        required_fields = ('pk_data', 'fk_pt_institutional_id', 'fk_transplant_day_zero',
                           'fk_transplant_start_weight_data_type', 'fk_transplant_start_weight', 'fk_data_type',
                           'data_value', 'data_date')

        for field in required_fields:
            if field not in field_names:
                return False
        return True

    # create record in database
    def create_account_in_db(self, dict_data):
        list_data = []
        result = False
        rows_error = 0
        for record in dict_data:
            pk_data = record['pk_data']
            fk_institution_id = record['fk_pt_institutional_id']
            pk_transplant_day_zero = record['fk_transplant_day_zero']
            fk_transplant_start_weight = record['fk_transplant_start_weight_data_type']
            fk_data_type = record['fk_data_type']
            data_value = record['data_value']
            data_date = record['data_date']

            account = Transplant(day_zero=pk_transplant_day_zero, start_weight=data_value)

            list_data.append(account)

        if list_data:
            # bulk_create will create multiple object in a single query
            created_accounts = Transplant.objects.bulk_create(list_data)

            if len(list_data) == len(created_accounts):
                result = True
            else:
                rows_error = len(list_data) - len(created_accounts)

        return result, rows_error

    # validates the extension of a given file
    def validate_file_extension(self, value, extension):
        if value.endswith(extension):
            return True
        return False