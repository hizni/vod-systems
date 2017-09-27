from django.shortcuts import render, redirect

from django.template import Context
from django.contrib.auth import authenticate
from django.template.context_processors import csrf
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, UpdateView

from user_forms import UserCreateForm, UserUpdateForm, UserRetireForm
from parsley.decorators import parsleyfy


def login(request):
    context = Context({})
    context.update(csrf(request))
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username is not None:
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('user-list')
        else:
            # return render(request, 'vod/login.html', context)
            messages.add_message(request, messages.WARNING, 'User could not be logged in.')
            context.update({'messages': messages.get_messages(request)})
            return render(request, './vod/login.html', context)
    else:
        messages.add_message(request, messages.WARNING, 'Please enter a username and/or password.')
        context.update({'messages': messages.get_messages(request)})
        return render(request, './vod/login.html', context)


"""
User model Class Based Views
    UserListView    - list all the users
    
    UserCreateView  - create a new user
    UserUpdateView  - update a select user
    UserRetireView  - activate/deactivate the selected user 
"""


class UserListView(ListView):
    model = User
    template_name = './vod/admin/user-list.html'

    def get_queryset(self):
        return User.objects.all()


class UserCreateView(CreateView):
    form_class = parsleyfy(UserCreateForm)
    template_name = './vod/admin/generic-modal.html'
    view_title = 'Create new user'

    def form_valid(self, form):
        form.save()
        return redirect('user-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form,))


class UserUpdateView(UpdateView):

    form_class = parsleyfy(UserUpdateForm)
    model = User
    template_name = './vod/admin/generic-modal.html'
    view_title = 'Update existing user'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(UserUpdateView, self).get_form(form_class)
        form.helper.form_action = reverse('user-update', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return User.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('user-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))


class UserRetireView(UpdateView):
    form_class = parsleyfy(UserRetireForm)
    model = User
    template_name = './vod/admin/generic-modal.html'
    view_title = 'User active status'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(UserRetireView, self).get_form(form_class)
        form.helper.form_action = reverse('user-retire', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return User.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('user-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))

