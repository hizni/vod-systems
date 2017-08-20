from django.shortcuts import render, redirect

from django.template import Context
from django.contrib.auth import authenticate
from django.template.context_processors import csrf
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

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
            # return redirect('admin-user')
            return redirect(reverse('admin') + '?context=user')
        else:
            # return render(request, 'vod/login.html', context)
            messages.add_message(request, messages.WARNING, 'User could not be logged in.')
            context.update({'messages': messages.get_messages(request)})
            return render(request, './vod/login.html', context)
    else:
        messages.add_message(request, messages.WARNING, 'Please enter a username and/or password.')
        context.update({'messages': messages.get_messages(request)})
        return render(request, './vod/login.html', context)


def admin(request):
    context_code = request.GET.get('context')

    # gather data
    if context_code == 'user':
        data = User.objects.all()
        create_form = ExtendedUserCreationForm()
    elif context_code == 'institution':
        data = Institution.objects.all()
        create_form = []
    elif context_code == 'alias_identifier':
        data = AliasIdentifier.objects.all()
        create_form = []
    elif context_code == 'transplant':
        data = TransplantType.objects.all()
        create_form = []
    elif context_code == 'datatype':
        data = DataType.objects.all()
        create_form = []
    else:
        data = []
        create_form = []

    context = {'context': context_code, 'data': data, 'create_form': create_form}
    return render(request, "./vod/admin.html", context)


def add_data(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    return redirect(reverse('admin') + '?context=user')



