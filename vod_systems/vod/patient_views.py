from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.shortcuts import render, redirect,HttpResponseRedirect
from models import Patient, Patient_Identifier ,User_Institution, Patient_Transplant, Transplant_Type, Alias_Identifier, Institution
from django.core.urlresolvers import reverse

from patient_forms import PatientCreateUpdateForm, PatientRetireForm, PatientAliasCreateForm, \
    PatientTransplantCreateForm

from parsley.decorators import parsleyfy

"""
Patient model Class Based Views
    PatientListView    - list all the data types

    PatientCreateView  - create a new data type
    PatientUpdateView  - update a selected data type
    PatientRetireView  - activate/deactivate the selected data type
    
    PatientIdentifiersListView - list all identifiers for a selected patient
    PatientAliasCreateView - create a new alias for a patient
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


class PatientIdentifiersDetailView(DetailView):
    model = Patient
    template_name = './vod/user/patient-detail.html'
    view_title = 'Add new patient identifier'
    selected_pk = 0

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return Patient.objects.get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(PatientIdentifiersDetailView, self).get_context_data(**kwargs)
        context['patient_ids'] = Patient_Identifier.objects.filter(fk_patient_id=self.kwargs['id'])
        context['patient_transplants'] = Patient_Transplant.objects.filter(fk_patient_id=self.kwargs['id'])
        return context


class PatientAliasCreateView(CreateView):
    form_class = parsleyfy(PatientAliasCreateForm)
    template_name = '../templates/common/modal-template.html'
    view_title = 'Create patient alias'

    def get_form_kwargs(self):
        kwargs = super(PatientAliasCreateView, self).get_form_kwargs()
        kwargs['pid'] = self.kwargs['id']
        return kwargs

    def get_form(self, form_class):
        form = super(PatientAliasCreateView, self).get_form(form_class)
        # form.fields['fk_institution_id'].queryset = User_Institution.objects.filter(fk_user_id=self.request.user.id)

        form.fields['fk_identifier_type'].queryset = Alias_Identifier.objects.all()
        form.fields['fk_patient_id'].initial = Patient.objects.get(id=self.kwargs['id'])
        return form

    def form_valid(self, form):
        form.save()
        return redirect('patient-detail', id=self.kwargs['id'])

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form ,))


class PatientTransplantCreateView(CreateView):
    form_class = parsleyfy(PatientTransplantCreateForm)
    template_name = '../templates/common/modal-template.html'
    view_title = 'Create new transplant'

    def get_form_kwargs(self):
        kwargs = super(PatientTransplantCreateView, self).get_form_kwargs()
        kwargs['pid'] = self.kwargs['id']
        return kwargs

    def get_form(self, form_class):
        form = super(PatientTransplantCreateView,self).get_form(form_class)

        form.fields['fk_transplant_type'].queryset = Transplant_Type.objects.all()
        form.fields['fk_patient_id'].initial = Patient.objects.get(id=self.kwargs['id'])
        return form

    def form_valid(self, form):
        form.save()
        return redirect('patient-detail', id=self.kwargs['id'])

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))


class PatientCreateView(CreateView):
    form_class = parsleyfy(PatientCreateUpdateForm)
    template_name = '../templates/common/modal-template.html'
    view_title = 'Create new patient'

    def get_form(self, form_class):
        form = super(PatientCreateView, self).get_form(form_class)
        # form.fields['fk_institution_id'].queryset = User_Institution.objects.filter(fk_user_id=self.request.user.id)
        form.fields['fk_institution_id'].queryset = Institution.objects.all().filter(id=User_Institution.objects.filter(fk_user_id=self.request.user.id).values('fk_institution_id'))
        return form

    def form_valid(self, form):
        form.save()
        return redirect('patient-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form,))


class PatientUpdateView(UpdateView):

    form_class = parsleyfy(PatientCreateUpdateForm)
    model = Patient
    template_name = '../templates/common/modal-template.html'
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
    template_name = '../templates/common/modal-template.html'
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
