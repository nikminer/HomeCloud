from django.shortcuts import redirect,render
from .directory import isAccess,getPathHierrarhy
from HomeCloud.views import getDiskspace
from ..forms import UploadFileForm
from .uploads import handle_uploaded_file
from .Preview import GetCode
import shutil
import os
import json
import datetime


from django.contrib.auth.decorators import login_required
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            for f in form.files.getlist('File'):
                handle_uploaded_file(f,request.POST['path'],request)
            return redirect(request.scheme + "://" +request.get_host()+"/file/explorer"+request.POST['path'])
    explorer(request,request.POST['path'])



conf=json.loads(open("static/config/Groups.json","r").read())
@login_required
def back(request,path):
    if path=="/":
        redirect(request.scheme + "://" +request.get_host())
    else:
        return redirect(request.scheme + "://" +request.get_host()+"/file/explorer"+os.path.split(path)[0])


@login_required
def explorer(request, path):

    DirList=[]
    FileList=Files()
    GroupQueue={}
    QueueIndex=0
    
    path= os.path.splitdrive(os.path.expanduser(path).replace('\\','/'))[1]
    for i in conf:
        for i1 in conf[i]['formats']:
            FileList.formats.update({i1:i})
        FileList.groups.append(Groupe(i,conf[i]['icon']))
        GroupQueue.update({i:QueueIndex})
        QueueIndex+=1
    FileList.groups.append(Groupe("Others","images/file.png"))
    GroupQueue.update({"Other":QueueIndex})
    
    for i in os.listdir(path):
        if path=="/":
            path=""
        if os.path.isdir(os.path.abspath(path+"/"+i)) and isAccess(os.path.abspath(path+"/"+i)):
            DirList.append(Dirictory(i,os.path.getctime(path+"/"+i)))
        elif os.path.isfile(os.path.abspath(path+"/"+i)) and os.access(os.path.abspath(path+"/"+i),os.R_OK):
            i1=FileList.formats.get(i.split(".")[-1].upper())
            if i1:
                if (i1=="Pictures"):
                    FileList.groups[GroupQueue[i1]].list.append(Image(i,os.path.getsize(path+"/"+i),os.path.getctime(path+"/"+i),GetCode(path+"/"+i)))
                else:
                    FileList.groups[GroupQueue[i1]].list.append(fileobj(i,os.path.getsize(path+"/"+i),os.path.getctime(path+"/"+i)))
            else:
                FileList.groups[GroupQueue["Other"]].list.append(fileobj(i,os.path.getsize(path+"/"+i),os.path.getctime(path+"/"+i)))
        
    return render(request, "File/explorer.html", 
    {
        "dirs": DirList,
        "disk":getDiskspace,
        "files":FileList,
        "path":path,
        "host":request.scheme + "://" +request.get_host(),
        "pathes":getPathHierrarhy(path),
        "forms":UploadFileForm()
    })

class Files:
    groups=[]
    formats={}
    def __init__(self):
        self.groups=[]
        self.formats={}

class Dirictory:
    name=""
    date=""
    def __init__(self,name,date):
        self.name=name
        self.date= datetime.date.fromtimestamp(date)

class Groupe(object):
    name=""
    icon=""
    list=[]
    def __init__(self,name,icon):
        self.name=name
        self.list=[]
        self.icon=icon

class fileobj(object):
    name=""
    size=0
    date=""
    def __init__(self,name,size,date):
        self.name=name
        self.size=size
        self.date= datetime.date.fromtimestamp(date)

class Image(fileobj):
    code=""
    def __init__(self,name,size,date,code):
        super().__init__(name,size,date)
        self.code=code
        