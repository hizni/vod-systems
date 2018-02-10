from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect

from models import User_Institution, Institution, Datatype, Transplant_Type, Alias_Identifier, Data_Cleansing_Template, Data_Cleansing_Template_Field, User
from django.core.urlresolvers import reverse

from institution_forms import InstitutionCreateUpdateForm, InstitutionRetireForm
from parsley.decorators import parsleyfy
"""
Institution model Class Based Views
    InstitutionListView    - list all the institutions

    InstitutionCreateView  - create a new institution
    InstitutionUpdateView  - update a selected institution
    InstitutionRetireView  - activate/deactivate the selected institution 
"""


class InstitutionListView(ListView):
    model = Institution
    template_name = './vod/admin/institution-list.html'

    def get_queryset(self):
        return Institution.objects.all()

    def get_context_data(self, **kwargs):
         context = super(InstitutionListView, self).get_context_data(**kwargs)
         context['users'] = User.objects.all().count()
         context['institutions'] = Institution.objects.all().count()
         context['alias_identifiers'] = Alias_Identifier.objects.all().count()
         context['user_institutions'] = User_Institution.objects.all().filter(fk_user_id=self.request.user.id).count()
         context['datatypes'] = Datatype.objects.all().count()
         context["transplants"] = Transplant_Type.objects.all().count()
         context['cleansing_templates'] = Data_Cleansing_Template.objects.all().count()
         # context['patients'] = Patient.objects.all().filter(fk_institution_id=context["user_institutions"])
         return context


class InstitutionCreateView(CreateView):
    form_class = parsleyfy(InstitutionCreateUpdateForm)
    template_name = '../templates/common/modal-template.html'
    view_title = 'Create new institution'

    def form_valid(self, form):
        form.save()
        return redirect('institution-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form ,))


class InstitutionUpdateView(UpdateView):

    form_class = parsleyfy(InstitutionCreateUpdateForm)
    model = Institution
    template_name = '../templates/common/modal-template.html'
    view_title = 'Update existing institution'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(InstitutionUpdateView, self).get_form(form_class)
        form.helper.form_action = reverse('institution-update', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return Institution.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('institution-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))


class InstitutionRetireView(UpdateView):
    form_class = parsleyfy(InstitutionRetireForm)
    model = Institution
    template_name = '../templates/common/modal-template.html'
    view_title = 'Institution active status'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(InstitutionRetireView, self).get_form(form_class)
        form.helper.form_action = reverse('institution-retire', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return Institution.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('institution-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))

