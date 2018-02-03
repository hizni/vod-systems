from django.views.generic import ListView, View
from django.shortcuts import render, redirect
from django.db import models

from models import Raw_Uploaded_Data

"""
Institution model Class Based Views
    InstitutionListView    - list all the institutions

    InstitutionCreateView  - create a new institution
    InstitutionUpdateView  - update a selected institution
    InstitutionRetireView  - activate/deactivate the selected institution 
"""


class RawDataListView(ListView):
    model = Raw_Uploaded_Data
    template_name = './vod/user/raw-data-list.html'

    def get_queryset(self):
        return Raw_Uploaded_Data.objects.all()

# class DataTypeCreateView(CreateView):
#     form_class = parsleyfy(DatatypeCreateUpdateForm)
#     template_name = '../templates/common/modal-template.html'
#     view_title = 'Create new data type'
#
#     def form_valid(self, form):
#         form.save()
#         return redirect('datatype-list')
#
#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form ,))


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
