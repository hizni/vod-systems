from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.apps import apps
from vod.models import Data_Cleansing_Template, Data_Cleansing_Template_Field


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def dataCleansingTemplateFields_asJSON(request):
    json = serializers.serialize('json', [])
    try:
        template = Data_Cleansing_Template.objects.get(id=request.GET.get('id', None))
        field_list = Data_Cleansing_Template_Field.objects.all().filter(fk_cleansing_template_id=template)
        if field_list:
            json = serializers.serialize('json', field_list)

        return HttpResponse(json, content_type='application/json')
    except Data_Cleansing_Template.DoesNotExist:
        return HttpResponse(json, content_type='application/json')

def modelsInApp(request):
    myapp = apps.get_app_config('vod')
    return HttpResponse(myapp.models, content_type='application/json')


