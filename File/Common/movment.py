from django.shortcuts import redirect,render
from .directory import isAccess,getPathHierrarhy
import shutil
import os
import json

def back(request,path):
    if path=="\\":
        redirect("http://"+request.get_host())
    else:
        return redirect("http://"+request.get_host()+"/file/explorer"+os.path.split(path)[0])

def explorer(request, path):

    DirList=[]
    FileList=Files()
    GroupQueue={}
    QueueIndex=0

    path= os.path.splitdrive(os.path.expanduser(path).replace("\\","/"))[1]
    
    conf=json.loads(open("static/config/Groups.json","r").read())
    for i in conf:
        for i1 in conf[i]['formats']:
            FileList.formats.update({i1:i})
        FileList.groups.append(Groupe(i,conf[i]['icon']))
        GroupQueue.update({i:QueueIndex})
        QueueIndex+=1
    FileList.groups.append(Groupe("Others","images/file.png"))
    GroupQueue.update({"Other":QueueIndex})
    
    for i in os.listdir(path):
        if os.path.isdir(os.path.abspath(path+"\\"+i)) and isAccess(os.path.abspath(path+"\\"+i)):
            DirList.append(i)
        elif os.path.isfile(os.path.abspath(path+"\\"+i)) and os.access(os.path.abspath(path+"\\"+i),os.R_OK):
            i1=FileList.formats.get(i.split(".")[-1].upper())
            if i1:
                FileList.groups[GroupQueue[i1]].list.append(fileobj(i,os.path.getsize(path+"\\"+i)))
            else:
                FileList.groups[GroupQueue["Other"]].list.append(fileobj(i,os.path.getsize(path+"\\"+i)))
    if path=="/":
        path=""
    return render(request, "File/explorer.html", 
    {
        "dirs": DirList,
        "files":FileList,
        "path":path,
        "host":"http://"+request.get_host(),
        "pathes":getPathHierrarhy(path),
    })

class Files:
    groups=[]
    formats={}
    def __init__(self):
        self.groups=[]
        self.formats={}

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
    def __init__(self,name,size):
        self.name=name
        self.size=size