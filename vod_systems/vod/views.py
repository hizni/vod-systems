from django.shortcuts import render, render_to_response
from django.template import Context
from django.contrib.auth import authenticate
from django.template.context_processors import csrf
from django.contrib.auth import login as auth_login
from django.contrib import messages


def login(request):
    context = Context({})
    context.update(csrf(request))
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username is not None:
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, 'vod/admin_home.html')
            # {'name': request.user.username})
        else:
            # return render(request, 'vod/login.html', context)
            messages.success(request, "User could not be logged in.")
            return render_to_response("vod/login.html", context)
    else:
        messages.success(request, "Please enter a username and/or password.")
        return render_to_response("vod/login.html", context)

"""
def home(request):
    context = Context({})
    return render(request, "vod/home.html", context)
"""