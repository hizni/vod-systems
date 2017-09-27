from django.conf.urls import url
from vod import views
from vod.views import UserListView, UserCreateView, UserUpdateView, UserRetireView

urlpatterns = [
    url(r'login', views.login, name='vod-login'),

    url(r'^user/list/$', UserListView.as_view(), name='user-list'),
    url(r'^user/create/$', UserCreateView.as_view(), name='user-create'),
    url(r'^user/update/(?P<id>\d+)/$', UserUpdateView.as_view(), name='user-update'),
    url(r'^user/delete/(?P<id>\d+)/$', UserRetireView.as_view(), name='user-retire'),
]