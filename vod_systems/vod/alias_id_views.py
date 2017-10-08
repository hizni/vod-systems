from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect

from models import AliasIdentifier
from django.core.urlresolvers import reverse

from alias_id_forms import AliasIdCreateUpdateForm, AliasIdRetireForm
from parsley.decorators import parsleyfy

"""
Alias Identifier model Class Based Views
    AliasIdListView    - list all the alias identifier

    AliasIdCreateView  - create a new alias identifier
    AliasIdpdateView  - update a selected alias identifier
    AliasIdRetireView  - activate/deactivate the selected alias identifier 
"""


class AliasIdListView(ListView):
    model = AliasIdentifier
    template_name = './vod/admin/alias-id-list.html'

    def get_queryset(self):
        return AliasIdentifier.objects.all()


class AliasIdCreateView(CreateView):
    form_class = parsleyfy(AliasIdCreateUpdateForm)
    template_name = './vod/admin/generic-modal.html'
    view_title = 'Create new Alias Identifier'

    def form_valid(self, form):
        form.save()
        return redirect('alias-id-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form ,))


class AliasIdUpdateView(UpdateView):

    form_class = parsleyfy(AliasIdCreateUpdateForm)
    model = AliasIdentifier
    template_name = './vod/admin/generic-modal.html'
    view_title = 'Update existing Alias Identifier'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(AliasIdUpdateView, self).get_form(form_class)
        form.helper.form_action = reverse('alias-id-update', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return AliasIdentifier.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('alias-id-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))


class AliasIdRetireView(UpdateView):
    form_class = parsleyfy(AliasIdRetireForm)
    model = AliasIdentifier
    template_name = './vod/admin/generic-modal.html'
    view_title = 'Alias Identifier active status'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(AliasIdRetireView, self).get_form(form_class)
        form.helper.form_action = reverse('alias-id-retire', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return AliasIdentifier.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('alias-id-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))
