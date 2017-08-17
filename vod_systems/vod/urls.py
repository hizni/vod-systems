from django.conf.urls import url
from vod import views


urlpatterns = [
    url(r'login', views.login, name='vod-login'),

    url(r'admin', views.admin, name='admin'),
]