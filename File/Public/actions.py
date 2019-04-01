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

@login_required
def SwithVisFile(request):
        userfile=Publicfile.objects.filter(Sharinguser=request.user).get(pseudoname=request.POST['ModalData'])
        userfile.isvisible=not userfile.isvisible== 'True'
        userfile.save()
        return HttpResponseRedirect("/file/public/share/getFiles")

@login_required
def DelPubFile(request):
        Publicfile.objects.filter(Sharinguser=request.user).get(pseudoname=request.POST['ModalData']).delete()
        return HttpResponseRedirect("/file/public/share/getFiles")

@login_required
def GetUserFile(request):
        Uflies=[]
        for i in Publicfile.objects.filter(Sharinguser=request.user):
                try:
                        size=os.path.getsize(i.path)
                except FileNotFoundError:
                        size=0

                Uflies.append(UserFile(pn=i.pk,size=size,path=i.path,visible=i.isvisible))

        return render(request, "Public/UserFileList.html", 
        {
                "host":request.scheme + "://" +request.get_host(),
                "list":Uflies
        })

def exist(request):
        return HttpResponse(not Publicfile.objects.filter(pseudoname=request.POST['name']).count()>0)
@login_required
def AddFile(request):
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
                "host":request.scheme + "://" +request.get_host(),
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
class UserFile:
        pn=""
        size=0
        visible=True
        path=""
        def __init__(self, pn, size,path, visible):
                self.pn=pn
                self.size=size
                self.path=path
                self.visible=visible
        