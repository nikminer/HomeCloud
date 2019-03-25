from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse,StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from File.models import Publicfile

import os
def action(request):
    print (request)

@login_required
def Shering(request,path):
        print ()
        return render(request, "Public/AddToPublic.html", 
        {
                'path':path,
                "host":request.scheme + "://" + request.get_host(),
        })

def exist(request):
        return HttpResponse(not Publicfile.objects.filter(pseudoname=request.POST['name']).count()>0)
@login_required
def AddFile(request):
        print(request.POST)
        print('isVisible' in request.POST.keys())
        Publicfile.objects.create(pseudoname=request.POST['name'],path=request.POST['path'],Sharinguser=request.user.username,isvisible='isVisible' in request.POST.keys()).save()
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
        path= Publicfile.objects.get(pseudoname=name).path
        response = StreamingHttpResponse(file_iterator(path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}{1}"'.format(name,os.path.splitext(path)[1])
        return response

def explorePublic(request):
        Pflies=[]
        for i in Publicfile.objects.filter(isvisible="True"):
                try:
                        Pflies.append(Public(pn=i.pk,user=i.Sharinguser,size=os.path.getsize(i.path)))
                except FileNotFoundError:
                        Publicfile.objects.get(pseudoname=i.pk).delete()

        return render(request, "Public/PublicList.html", 
        {
                "host":request.get_host(),
                "list":Pflies
        })

class Public:
        pn=""
        size=0
        user=""
        def __init__(self, pn,size,user):
                self.pn=pn
                self.size=size
                self.user=user