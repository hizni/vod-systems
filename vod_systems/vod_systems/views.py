from django.shortcuts import render
from django.template import Context


def landing(request):
    context = Context({})
    return render(request, "vod_systems/landing.html", context)