from django.views.generic import ListView
from django.shortcuts import render, redirect

from models import UploadHistory
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse


class UploadListView(ListView):
    model = UploadHistory
    template_name = './vod/user/upload-list.html'

    def get_queryset(self):
        return UploadHistory.objects.all()

    def post(self, request):
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            # return render(request, 'core/simple_upload.html', {'uploaded_file_url': uploaded_file_url})

            # return render(request, 'core/simple_upload.html')
        return redirect('upload-list')