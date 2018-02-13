from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from vod import user_views
from vod.alias_id_views import AliasIdListView, AliasIdCreateView, AliasIdUpdateView, AliasIdRetireView
from vod.datatype_views import DataTypeListView, DataTypeCreateView, DataTypeUpdateView, DataTypeRetireView
from vod.institution_views import InstitutionListView, InstitutionCreateView, InstitutionUpdateView, \
    InstitutionRetireView

from vod.patient_views import PatientListView, PatientCreateView, PatientUpdateView, PatientRetireView, \
    PatientIdentifiersDetailView, PatientAliasCreateView, PatientTransplantCreateView
from vod.transplant_views import TransplantListView, TransplantCreateView, TransplantUpdateView, TransplantRetireView
from vod.data_views import RawDataListView, RawDataProcessingView, DataAnalysisDetailView
from vod.cleansing_views import DataCleansingTemplatesListView, DataCleansingTemplateCreateView, DataCleansingTemplateFieldsUpdateView
from vod.upload_views import UploadListView
from vod.user_views import UserListView, UserCreateView, UserUpdateView, UserRetireView, LoginView
from vod import helper_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'login', LoginView.as_view(), name='vod-login'),
    url(r'logout', user_views.logout, name='vod-logout'),

    # url routes for superuser (admin) related views
    url(r'^user/list/$', login_required(UserListView.as_view()), name='user-list'),
    url(r'^user/create/$', login_required(UserCreateView.as_view()), name='user-create'),
    url(r'^user/update/(?P<id>\d+)/$', login_required(UserUpdateView.as_view()), name='user-update'),
    url(r'^user/delete/(?P<id>\d+)/$', login_required(UserRetireView.as_view()), name='user-retire'),

    url(r'^institution/list/$', login_required(InstitutionListView.as_view()), name='institution-list'),
    url(r'^institution/create/$', login_required(InstitutionCreateView.as_view()), name='institution-create'),
    url(r'^institution/update/(?P<id>\d+)/$', login_required(InstitutionUpdateView.as_view()), name='institution-update'),
    url(r'^institution/delete/(?P<id>\d+)/$', login_required(InstitutionRetireView.as_view()), name='institution-retire'),


    url(r'^aliasid/list/$', login_required(AliasIdListView.as_view()), name='alias-id-list'),
    url(r'^aliasid/create/$', login_required(AliasIdCreateView.as_view()), name='alias-id-create'),
    url(r'^aliasid/update/(?P<id>\d+)/$', login_required(AliasIdUpdateView.as_view()), name='alias-id-update'),
    url(r'^aliasid/delete/(?P<id>\d+)/$', login_required(AliasIdRetireView.as_view()), name='alias-id-retire'),

    url(r'^datatype/list/$', login_required(DataTypeListView.as_view()), name='datatype-list'),
    url(r'^datatype/create/$', login_required(DataTypeCreateView.as_view()), name='datatype-create'),
    url(r'^datatype/update/(?P<id>\d+)/$', login_required(DataTypeUpdateView.as_view()), name='datatype-update'),
    url(r'^datatype/delete/(?P<id>\d+)/$', login_required(DataTypeRetireView.as_view()), name='datatype-retire'),

    url(r'^transplant/list/$', login_required(TransplantListView.as_view()), name='transplant-list'),
    url(r'^transplant/create/$', login_required(TransplantCreateView.as_view()), name='transplant-create'),
    url(r'^transplant/update/(?P<id>\d+)/$', login_required(TransplantUpdateView.as_view()), name='transplant-update'),
    url(r'^transplant/delete/(?P<id>\d+)/$', login_required(TransplantRetireView.as_view()), name='transplant-retire'),

    # url routes for staff (normal user) related views
    url(r'^upload/list/$', login_required(UploadListView.as_view()), name='upload-list'),

    url(r'^patient/list/$', login_required(PatientListView.as_view()), name='patient-list'),
    url(r'^patient/create/$', login_required(PatientCreateView.as_view()), name='patient-create'),
    url(r'^patient/update/(?P<id>\d+)/$', login_required(PatientUpdateView.as_view()), name='patient-update'),
    url(r'^patient/delete/(?P<id>\d+)/$', login_required(PatientRetireView.as_view()), name='patient-retire'),

    url(r'^patient/create-alias/(?P<id>\d+)/$', login_required(PatientAliasCreateView.as_view()), name='patient-create-alias'),
    url(r'^patient/create-transplant/(?P<id>\d+)/$', login_required(PatientTransplantCreateView.as_view()), name='patient-create-transplant'),

    url(r'^patient/detail/(?P<id>\d+)/$', login_required(PatientIdentifiersDetailView.as_view()), name='patient-detail'),

    # url routes to view data
    url(r'^data/uploaded-raw/$', login_required(RawDataListView.as_view()), name='raw-data-list'),
    # url(r'^data/uploaded-raw/complete/(?P<id>\d+)/$', login_required(RawDataProcessingView.as_view()), name='data-complete'),
    # url(r'^data/uploaded-raw/valid/(?P<id>\d+)/$', login_required(RawDataProcessingView.as_view()), name='data-valid'),
    url(r'^data/detail/(?P<id>\d+)/(?P<tid>\d+)/$', login_required(DataAnalysisDetailView.as_view()), name='data-analysis-detail'),
    url(r'^data/cleansing-profile/$', login_required(DataCleansingTemplatesListView.as_view()), name='cleansing-profile-list'),
    # url(r'^data/cleansing-profile/create/$', login_required(DataCleansingTemplateCreateView.as_view()), name='cleansing-profile-create'),
    # url(r'^data/cleansing-profile/detail/(?P<id>\d+)/$', login_required(DataCleansingTemplateFieldsListView.as_view()), name='cleansing-profile-detail'),
    url(r'^data/cleansing-profile/detail/update/(?P<id>\d+)/$', login_required(DataCleansingTemplateFieldsUpdateView.as_view()), name='cleansing-template-field-update'),


    # route to helper views
    url(r'^ajax/validate_username/$', helper_views.validate_username, name='validate_username'),
    url(r'^ajax/cleansing-profile-detail/$', helper_views.dataCleansingTemplateFields_asJSON, name='ajax-cleansing-profile-detail'),
    url(r'^ajax/models/$', helper_views.modelsInApp, name='app-models'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)