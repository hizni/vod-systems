from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect

from models import Alias_Identifier
from django.core.urlresolvers import reverse
from models import User_Institution, Institution, Datatype, Transplant_Type, Alias_Identifier, Data_Cleansing_Template, Data_Cleansing_Template_Field, User
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
    model = Alias_Identifier
    template_name = './vod/admin/alias-id-list.html'

    def get_queryset(self):
        return Alias_Identifier.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AliasIdListView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all().count()
        context['institutions'] = Institution.objects.all().count()
        context['alias_identifiers'] = Alias_Identifier.objects.all().count()
        context['user_institutions'] = User_Institution.objects.all().filter(fk_user_id=self.request.user.id).count()
        context['datatypes'] = Datatype.objects.all().count()
        context["transplants"] = Transplant_Type.objects.all().count()
        context['cleansing_templates'] = Data_Cleansing_Template.objects.all().count()
        # context['patients'] = Patient.objects.all().filter(fk_institution_id=context["user_institutions"])
        return context

class AliasIdCreateView(CreateView):
    form_class = parsleyfy(AliasIdCreateUpdateForm)
    template_name = '../templates/common/modal-template.html'
    view_title = 'Create new Alias Identifier'

    def form_valid(self, form):
        form.save()
        return redirect('alias-id-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form ,))


class AliasIdUpdateView(UpdateView):

    form_class = parsleyfy(AliasIdCreateUpdateForm)
    model = Alias_Identifier
    template_name = '../templates/common/modal-template.html'
    view_title = 'Update existing Alias Identifier'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(AliasIdUpdateView, self).get_form(form_class)
        form.helper.form_action = reverse('alias-id-update', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return Alias_Identifier.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('alias-id-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))


class AliasIdRetireView(UpdateView):
    form_class = parsleyfy(AliasIdRetireForm)
    model = Alias_Identifier
    template_name = '../templates/common/modal-template.html'
    view_title = 'Alias Identifier active status'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(AliasIdRetireView, self).get_form(form_class)
        form.helper.form_action = reverse('alias-id-retire', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return Alias_Identifier.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('alias-id-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))
