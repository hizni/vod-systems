from django.conf.urls import url
from vod import views
from vod.views import UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserRetireView

urlpatterns = [
    url(r'login', views.login, name='vod-login'),

    url(r'^list/$', UserListView.as_view(), name='user-list'),
    url(r'^create-user/$', UserCreateView.as_view(), name='user-create'),
    url(r'^update-user/(?P<id>\d+)/$', UserUpdateView.as_view(), name="user-update"),
    url(r'^retire-user/(?P<id>\d+)/$', UserRetireView.as_view(), name="user-retire"),
    url(r'^delete-user/(?P<id>\d+)/$', UserDeleteView.as_view(), name="user-delete"),
]