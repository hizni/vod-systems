from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect

from models import Institution
from django.core.urlresolvers import reverse


from parsley.decorators import parsleyfy
"""
UserInstitution model Class Based Views
    InstitutionListView    - list all the institutions

    InstitutionCreateView  - create a new institution
    InstitutionUpdateView  - update a selected institution
    InstitutionRetireView  - activate/deactivate the selected institution 
"""


class UserInstitutionListView(ListView):
    model = Institution
    template_name = './vod/admin/user-institution-list.html'

    def get_queryset(self):
        return Institution.objects.all()

