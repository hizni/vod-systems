from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.db import models

from models import Raw_Uploaded_Data, Patient_Identifier, Patient, Transplant_Type, Patient_Transplant


class DataAnalysisDetailView(DetailView):
    model = Raw_Uploaded_Data
    template_name = './vod/user/data-detail.html'
    view_title = 'Data analysis details'
    selected_pt_pk = 0
    selected_transplant_num = 0
    selected_transplant_type = 0

    def get_queryset(self):
        patientTransplant = Patient_Transplant.objects.filter(id=self.request.user.id)
        return patientTransplant

    def get_object(self, queryset=None):
        # passed the pk ID for the patient object being looked at
        self.selected_pt_pk = self.kwargs['id']
        self.selected_transplant_pk = self.kwargs['tid']

        transplant = Patient_Transplant.objects.get(id=self.kwargs['tid'])

        self.selected_transplant_num = transplant.number
        self.selected_transplant_type_code = transplant.fk_transplant_type.code

        return Patient_Transplant.objects.get(id=self.kwargs['tid'])

    def get_context_data(self, **kwargs):
        context = super(DataAnalysisDetailView, self).get_context_data(**kwargs)

        # passed the patient PK relating to the patient record
        # print(self.selected_pt_pk)
        # print(self.selected_transplant_num)
        # print(self.selected_transplant_type)

        pat_ids = Patient_Identifier.objects.filter(fk_patient_id=Patient.objects.filter(id=self.selected_pt_pk))
        # transplantType = Transplant_Type.objects.filter(id=self.selected_transplant_type)

        for p in pat_ids:
            context['analysis_bilirubin'] = Raw_Uploaded_Data.objects.filter(fk_data_type='serum-total-bilirubin-micromol-litre',
                                                                             fk_pt_identifier_type=p.fk_identifier_type.code,
                                                                             fk_pt_identifier_type_value=p.pt_identifier_type_value,
                                                                             fk_transplant_number=self.selected_transplant_num,
                                                                             fk_transplant_type=self.selected_transplant_type_code
                                                                            )

            context['analysis_renal_fn'] = Raw_Uploaded_Data.objects.filter(fk_data_type='renal-function-creatinine-clearance',
                                                                                  fk_pt_identifier_type=p.fk_identifier_type.code,
                                                                                  fk_pt_identifier_type_value=p.pt_identifier_type_value,
                                                                                  fk_transplant_number=self.selected_transplant_num,
                                                                                  fk_transplant_type=self.selected_transplant_type_code
                                                                                 )

            context['analysis_weight'] = Raw_Uploaded_Data.objects.filter(fk_data_type='weight-kilos',
                                                                          fk_pt_identifier_type=p.fk_identifier_type.code,
                                                                          fk_pt_identifier_type_value=p.pt_identifier_type_value,
                                                                          fk_transplant_number=self.selected_transplant_num,
                                                                          fk_transplant_type=self.selected_transplant_type_code
                                                                         )

            context['analysis_blood_alanine_transaminases'] = Raw_Uploaded_Data.objects.filter(
                                                                          fk_data_type='blood-alanine-transaminases',
                                                                          fk_pt_identifier_type=p.fk_identifier_type.code,
                                                                          fk_pt_identifier_type_value=p.pt_identifier_type_value,
                                                                          fk_transplant_number=self.selected_transplant_num,
                                                                          fk_transplant_type=self.selected_transplant_type_code
                                                                          )
        return context


class RawDataListView(ListView):
    model = Raw_Uploaded_Data
    template_name = './vod/user/raw-data-list.html'

    def get_queryset(self):
        return Raw_Uploaded_Data.objects.all()


class RawDataProcessingView(ListView):
    template_name = '../templates/common/modal-display-template.html'
    view_title = 'Raw Data Processor'
    selected_pk = 0

    # def get_object(self, queryset=None):
    #     self.selected_pk = self.kwargs['id']
    #     specific_upload_event =
    #     foobar_items = set()
    #
    #     foobar_items.add(specific_upload_event.upload_date)
    #     self.queryset = foobar_items
    #     # return Raw_Uploaded_Data.objects.get(id=self.kwargs['id'])
    #     return foobar_items

    def get_queryset(self):
        foobar_items = set()
        processingOutput = ProcessingTask.objects.none()

        # get the raw data for a particular upload event
        raw_uploaded_data = Raw_Uploaded_Data.objects.filter(fk_upload_history_id=self.kwargs['id'])
        row_count = 0

        # iterate over each row of uploaded data
        for row in raw_uploaded_data:
            # iterate over each row in the current field
            for field in row._meta.get_all_field_names():
                #print row._meta.get_field_by_name(field)
                # print row._meta.get_field('fk_transplant_day_zero')

                field_name = field
                field_value = getattr(row, field)

                pt = self.field_contains_empty(row_count, field, field_value, True)
                #foobar_items.add(pt)
                foobar_items.add(pt)
                #processingOutput.

                # print str(row_count) + str(field_name) + "=" + str(field_value)

            row_count = row_count + 1


        # return Raw_Uploaded_Data.objects.get(id=self.kwargs['id'])

        self.queryset = foobar_items
        return foobar_items

    def field_contains_empty(self, row_id, field_name, field_data, empty_allowed):
        pt = ProcessingTask()

        pt.upload_event_id = self.kwargs['id']
        pt.row_identifier = row_id
        pt.col_identifier = field_name

        pt.id = str(pt.upload_event_id) + str(pt.row_identifier) + str(pt.col_identifier)

        if field_data:
            pt.processing_outcome = 'not empty'
        else:
            pt.processing_outcome = 'EMPTY'

        return pt


class ProcessingTask(models.Model):
    upload_event_id = models.IntegerField,
    row_identifier = models.IntegerField,
    col_identifier = models.CharField(max_length=30),
    processing_outcome = models.CharField(max_length=25)
