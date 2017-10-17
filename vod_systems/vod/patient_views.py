from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.shortcuts import render, redirect
from models import Patient, Datatype, Patient_Identifier ,User_Institution
from django.core.urlresolvers import reverse

from patient_forms import PatientCreateUpdateForm, PatientRetireForm
from parsley.decorators import parsleyfy

"""
Patient model Class Based Views
    PatientListView    - list all the data types

    PatientCreateView  - create a new data type
    PatientUpdateView  - update a selected data type
    PatientRetireView  - activate/deactivate the selected data type
"""


class PatientListView(ListView):
    model = Patient
    template_name = './vod/user/patient-list.html'

    def get_queryset(self):
        user_insts = User_Institution.objects.values_list('fk_institution_id', flat=True).filter(fk_user_id=self.request.user.id)
        patients = Patient.objects.all().filter(fk_institution_id=user_insts)
        return patients

    def get_context_data(self, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)
        context['user_institutions_list'] = User_Institution.objects.all().filter(fk_user_id=self.request.user.id)
        return context


class PatientDetailView(DetailView):
    model = Patient
    template_name = './vod/user/patient-detail.html'


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
        return Patient.objects.get(id=self.kwargs['id'])

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
        return Patient.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('datatype-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))
