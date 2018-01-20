from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect

from models import Transplant_Type
from django.core.urlresolvers import reverse

from transplant_forms import TransplantCreateUpdateForm, TransplantRetireForm
from parsley.decorators import parsleyfy

"""
DataType model Class Based Views
    TransplantListView    - list all the data types

    TransplantCreateView  - create a new data type
    TransplantUpdateView  - update a selected data type
    TransplantRetireView  - activate/deactivate the selected data type
"""


class TransplantListView(ListView):
    model = Transplant_Type
    template_name = './vod/admin/transplant-list.html'

    def get_queryset(self):
        return Transplant_Type.objects.all()


class TransplantCreateView(CreateView):
    form_class = parsleyfy(TransplantCreateUpdateForm)
    template_name = '../templates/common/modal-template.html'
    view_title = 'Create new transplant'

    def form_valid(self, form):
        form.save()
        return redirect('transplant-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form ,))


class TransplantUpdateView(UpdateView):

    form_class = parsleyfy(TransplantCreateUpdateForm)
    model = Transplant_Type
    template_name = '../templates/common/modal-template.html'
    view_title = 'Update existing transplant'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(TransplantUpdateView, self).get_form(form_class)
        form.helper.form_action = reverse('transplant-update', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return Transplant_Type.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('transplant-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))


class TransplantRetireView(UpdateView):
    form_class = parsleyfy(TransplantRetireForm)
    model = Transplant_Type
    template_name = '../templates/common/modal-template.html'
    view_title = 'Transplant active status'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(TransplantRetireView, self).get_form(form_class)
        form.helper.form_action = reverse('transplant-retire', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return Transplant_Type.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('transplant-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))
