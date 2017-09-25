from django.conf.urls import url
from vod import views
from vod.views import UserListView, UserCreateView, UserUpdateView, \
    UserDeleteView, UserRetireView, AnotherCreateView, AnotherUpdateView

urlpatterns = [
    url(r'login', views.login, name='vod-login'),

    url(r'^list/$', UserListView.as_view(), name='user-list'),
    url(r'^create-user/$', UserCreateView.as_view(), name='user-create'),
    url(r'^update-user/(?P<id>\d+)/$', UserUpdateView.as_view(), name="user-update"),
    url(r'^retire-user/(?P<id>\d+)/$', UserRetireView.as_view(), name="user-retire"),
    url(r'^delete-user/(?P<id>\d+)/$', UserDeleteView.as_view(), name="user-delete"),

    url(r'^generic-modal/$', AnotherCreateView.as_view(), name='generic-modal'),
    url(r'^generic-update/(?P<id>\d+)/$', AnotherUpdateView.as_view(), name='generic-update'),
]