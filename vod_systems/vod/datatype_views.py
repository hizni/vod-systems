from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect

from models import DataType
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
    model = DataType
    template_name = './vod/admin/datatype-list.html'

    def get_queryset(self):
        return DataType.objects.all()


class DataTypeCreateView(CreateView):
    form_class = parsleyfy(DatatypeCreateUpdateForm)
    template_name = './vod/admin/generic-modal.html'
    view_title = 'Create new data type'

    def form_valid(self, form):
        form.save()
        return redirect('datatype-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form ,))


class DataTypeUpdateView(UpdateView):

    form_class = parsleyfy(DatatypeCreateUpdateForm)
    model = DataType
    template_name = './vod/admin/generic-modal.html'
    view_title = 'Update existing data type'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(DatatypeCreateUpdateForm, self).get_form(form_class)
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


class DataTypeRetireView(UpdateView):
    form_class = parsleyfy(DatatypeRetireForm)
    model = DataType
    template_name = './vod/admin/generic-modal.html'
    view_title = 'Data type active status'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(DatatypeRetireForm, self).get_form(form_class)
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
