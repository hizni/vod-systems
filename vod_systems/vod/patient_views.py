from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect
from models import Patient
from django.core.urlresolvers import reverse

from patient_forms import PatientCreateUpdateForm, PatientRetireForm
from parsley.decorators import parsleyfy

"""
DataType model Class Based Views
    DataTypeListView    - list all the data types

    DataTypeCreateView  - create a new data type
    DataTypeUpdateView  - update a selected data type
    DataTypeRetireView  - activate/deactivate the selected data type
"""


class PatientListView(ListView):
    model = Patient
    template_name = './vod/user/patient-list.html'

    def get_queryset(self):
        return Patient.objects.all()


class PatientCreateView(CreateView):
    form_class = parsleyfy(PatientCreateUpdateForm)
    template_name = '../templates/common/generic-modal.html'
    view_title = 'Create new patient'

    def form_valid(self, form):
        form.save()
        return redirect('patient-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form ,))


class PatientUpdateView(UpdateView):

    form_class = parsleyfy(PatientCreateUpdateForm)
    model = Patient
    template_name = '../templates/common/generic-modal.html'
    view_title = 'Update existing patient'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(PatientUpdateView, self).get_form(form_class)
        form.helper.form_action = reverse('datatype-update', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return DataType.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('datatype-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))


class PatientRetireView(UpdateView):
    form_class = parsleyfy(PatientRetireForm)
    model = Patient
    template_name = '../templates/common/generic-modal.html'
    view_title = 'Patient active status'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(PatientRetireView, self).get_form(form_class)
        form.helper.form_action = reverse('datatype-retire', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return DataType.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('datatype-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))
