from django.conf.urls import url
from vod import views

urlpatterns = [
    url(r'^', views.login),
]