from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from vod import user_views
from vod.alias_id_views import AliasIdListView, AliasIdCreateView, AliasIdUpdateView, AliasIdRetireView
from vod.datatype_views import DataTypeListView, DataTypeCreateView, DataTypeUpdateView, DataTypeRetireView
from vod.institution_views import InstitutionListView, InstitutionCreateView, InstitutionUpdateView, \
    InstitutionRetireView

from vod.patient_views import PatientListView, PatientCreateView, PatientUpdateView, PatientRetireView, \
    PatientIdentifiersDetailView, PatientAliasCreateView
from vod.transplant_views import TransplantListView, TransplantCreateView, TransplantUpdateView, TransplantRetireView
from vod.upload_views import UploadListView
from vod.user_views import UserListView, UserCreateView, UserUpdateView, UserRetireView, LoginView

from vod_systems import views

urlpatterns = [
    url(r'login', LoginView.as_view(), name='vod-login'),
    url(r'logout', views.landing, name='vod-logout'),

    # url routes for superuser (admin) related views
    url(r'^user/list/$', UserListView.as_view(), name='user-list'),
    url(r'^user/create/$', UserCreateView.as_view(), name='user-create'),
    url(r'^user/update/(?P<id>\d+)/$', UserUpdateView.as_view(), name='user-update'),
    url(r'^user/delete/(?P<id>\d+)/$', UserRetireView.as_view(), name='user-retire'),

    url(r'^institution/list/$', InstitutionListView.as_view(), name='institution-list'),
    url(r'^institution/create/$', InstitutionCreateView.as_view(), name='institution-create'),
    url(r'^institution/update/(?P<id>\d+)/$', InstitutionUpdateView.as_view(), name='institution-update'),
    url(r'^institution/delete/(?P<id>\d+)/$', InstitutionRetireView.as_view(), name='institution-retire'),


    url(r'^aliasid/list/$', AliasIdListView.as_view(), name='alias-id-list'),
    url(r'^aliasid/create/$', AliasIdCreateView.as_view(), name='alias-id-create'),
    url(r'^aliasid/update/(?P<id>\d+)/$', AliasIdUpdateView.as_view(), name='alias-id-update'),
    url(r'^aliasid/delete/(?P<id>\d+)/$', AliasIdRetireView.as_view(), name='alias-id-retire'),

    url(r'^datatype/list/$', DataTypeListView.as_view(), name='datatype-list'),
    url(r'^datatype/create/$', DataTypeCreateView.as_view(), name='datatype-create'),
    url(r'^datatype/update/(?P<id>\d+)/$', DataTypeUpdateView.as_view(), name='datatype-update'),
    url(r'^datatype/delete/(?P<id>\d+)/$', DataTypeRetireView.as_view(), name='datatype-retire'),

    url(r'^transplant/list/$', TransplantListView.as_view(), name='transplant-list'),
    url(r'^transplant/create/$', TransplantCreateView.as_view(), name='transplant-create'),
    url(r'^transplant/update/(?P<id>\d+)/$', TransplantUpdateView.as_view(), name='transplant-update'),
    url(r'^transplant/delete/(?P<id>\d+)/$', TransplantRetireView.as_view(), name='transplant-retire'),

    # url routes for staff (normal user) related views
    url(r'^upload/list/$', UploadListView.as_view(), name='upload-list'),

    url(r'^patient/list/$', PatientListView.as_view(), name='patient-list'),
    url(r'^patient/create/$', PatientCreateView.as_view(), name='patient-create'),
    url(r'^patient/update/(?P<id>\d+)/$', PatientUpdateView.as_view(), name='patient-update'),
    url(r'^patient/delete/(?P<id>\d+)/$', PatientRetireView.as_view(), name='patient-retire'),

    url(r'^patient/create-alias/(?P<id>\d+)/$', PatientAliasCreateView.as_view(), name='patient-create-alias'),

    url(r'^patient/detail/(?P<id>\d+)/$', PatientIdentifiersDetailView.as_view(), name='patient-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)