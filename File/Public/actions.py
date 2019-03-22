from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse,StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from File.models import Publicfile

import os
def action(request):
    print (request)

@login_required
def Shering(request,path):

    return render(request, "Public/AddToPublic.html", 
    {
        'path':path,
        "host":request.get_host(),
    })

def exist(request):
        return HttpResponse(not Publicfile.objects.filter(pseudoname=request.POST['name']).count()>0)
@login_required
def AddFile(request):
        print(request.POST)
        Publicfile.objects.create(pseudoname=request.POST['name'],path=request.POST['path'],Sharinguser=request.user.username,isvisible=request.POST['isVisible']).save()
        return HttpResponseRedirect("/file/public/")

def download(request,name):
        def file_iterator(file_name, chunk_size=512):
                with open(file_name,'rb') as f:
                        while True:
                                chunk = f.read(chunk_size)
                                if chunk:
                                        yield chunk
                                else:
                                        break
        path=Publicfile.objects.get(pseudoname=name).path
        print(path)
        response = StreamingHttpResponse(file_iterator(path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(os.path.split(path)[1])
        return response

def explorePublic(request):

    return render(request, "Public/PublicList.html", 
    {
        
    })