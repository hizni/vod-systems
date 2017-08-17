from django.shortcuts import render, redirect
from django.template import Context
from django.contrib.auth import authenticate
from django.template.context_processors import csrf
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User


def login(request):
    context = Context({})
    context.update(csrf(request))
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username is not None:
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('admin-home')
        else:
            # return render(request, 'vod/login.html', context)
            messages.add_message(request, messages.WARNING, 'User could not be logged in.')
            context.update({'messages': messages.get_messages(request)})
            # messages.success(request, "User could not be logged in.")
            return render(request, './vod/login.html', context)
    else:
        messages.add_message(request, messages.WARNING, 'Please enter a username and/or password.')
        # messages.success(request, "Please enter a username and/or password.")
        context.update({'messages': messages.get_messages(request)})
        return render(request, './vod/login.html', context)


def admin_home(request):
    return render(request, "./vod/admin_home.html", {'users': User.objects.all()})
