from django.shortcuts import render, redirect

from django.template import Context
from django.contrib.auth import authenticate
from django.template.context_processors import csrf
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from models import Institution, AliasIdentifier, TransplantType, DataType
from forms import ExtendedUserCreationForm


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
    UserCreateView  - create a new user
    UserListView    - list all the users
    UserUpdateView  - update a select user
    UserDeleteView  - delete the selected user 
"""


class UserListView(ListView):
    model = User
    template_name = './vod/admin/user-list.html'

    def get_queryset(self):
        return User.objects.all()


class UserCreateView(CreateView):
    model = User
    fields = '__all__'
    template_name = './vod/admin/user-create.html'

    def form_valid(self, form):
        object = form.save()
        # return render(self.request, 'user_create_success.html', {'fb': object})
        return redirect('user-list')


class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']
    template_name = './vod/admin/user-update.html'

    def dispatch(self, *args, **kwargs):
        self.id = kwargs['id']
        return super(UserUpdateView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('user-list')


class UserDeleteView(DeleteView):
    model = UserUpdateView
    template_name = './vod/admin/user-delete.html'

    def dispatch(self, *args, **kwargs):
        # self.id = kwargs['id']
        return super(UserDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        object = User.objects.get(id=self.kwargs['id'])
        return object

    def get_success_url(self):
        # return HttpResponseRedirect(reverse('admin-user-view'))
        return reverse('user-list')
