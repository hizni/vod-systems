from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect

from models import User_Institution, Institution, Datatype, Transplant_Type, Alias_Identifier, Data_Cleansing_Template, User
from django.core.urlresolvers import reverse

from datatype_forms import DatatypeCreateUpdateForm, DatatypeRetireForm
from parsley.decorators import parsleyfy

"""
DataType model Class Based Views
    DataTypeListView    - list all the data types

    DataTypeCreateView  - create a new data type
    DataTypeUpdateView  - update a selected data type
    DataTypeRetireView  - activate/deactivate the selected data type
"""


class DataTypeListView(ListView):
    model = Datatype
    template_name = './vod/admin/datatype-list.html'

    def get_queryset(self):
        return Datatype.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DataTypeListView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all().count()
        context['institutions'] = Institution.objects.all().count()
        context['alias_identifiers'] = Alias_Identifier.objects.all().count()
        context['user_institutions'] = User_Institution.objects.all().filter(fk_user_id=self.request.user.id).count()
        context['datatypes'] = Datatype.objects.all().count()
        context["transplants"] = Transplant_Type.objects.all().count()
        context['cleansing_templates'] = Data_Cleansing_Template.objects.all().count()
        # context['patients'] = Patient.objects.all().filter(fk_institution_id=context["user_institutions"])
        return context

class DataTypeCreateView(CreateView):
    form_class = parsleyfy(DatatypeCreateUpdateForm)
    template_name = '../templates/common/modal-template.html'
    view_title = 'Create new data type'

    def form_valid(self, form):
        form.save()
        return redirect('datatype-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form ,))


class DataTypeUpdateView(UpdateView):

    form_class = parsleyfy(DatatypeCreateUpdateForm)
    model = Datatype
    template_name = '../templates/common/modal-template.html'
    view_title = 'Update existing data type'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(DataTypeUpdateView, self).get_form(form_class)
        form.helper.form_action = reverse('datatype-update', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return Datatype.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('datatype-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))


class DataTypeRetireView(UpdateView):
    form_class = parsleyfy(DatatypeRetireForm)
    model = Datatype
    template_name = '../templates/common/modal-template.html'
    view_title = 'Data type active status'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(DataTypeRetireView, self).get_form(form_class)
        form.helper.form_action = reverse('datatype-retire', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return Datatype.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('datatype-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))
