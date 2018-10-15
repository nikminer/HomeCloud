from django.shortcuts import render,redirect
from django.http import HttpResponse
import base64

import os


def explorer(request, path):
    DirList=[]
    FileList=[]

    for i in os.listdir(path):
        if os.path.isdir(os.path.abspath(path+"\\"+i)) and isAccess(os.path.abspath(path+"\\"+i)):
            DirList.append(i)
        elif os.path.isfile(os.path.abspath(path+"\\"+i)):
            FileList.append(i)

    if path=="/":
        path=""

    return render(request, "File/explorer.html", 
    {
        "dirs": DirList,
        "files":FileList,
        "path":path,
        "host":"http://"+request.get_host()+"/file",
        "pathes":getPathHierrarhy(path)
    })
def view1(request, path):
    image = open(path,"rb").read()
    base=str(base64.encodestring(image),"utf-8")
    
    return render(request, "File/filePreview.html", 
    {   
        "hash":base,
        "host":"http://"+request.get_host()+"/file",
    })

def isAccess(path):
    try:
        os.listdir(path)
        return True
    except PermissionError:
        return False

def getPathHierrarhy(fullPath):
    pathes=[]
    currpath=""
    print(fullPath)
    if fullPath:
        for dir in fullPath[1:].split("/"):
            path=Path()
            path.dir=dir
            currpath+=dir+"/"
            path.hierrarhy=currpath
            pathes.append(path)
            pathes[-1].hierrarhy=pathes[-1].hierrarhy[0:-1]
        return pathes
class Path:
    dir=""
    hierrarhy=""
def back(request,path):
    print (os.path.split(path)[0])
    if path=="\\":
        redirect("http://"+request.get_host())
    else:
        return redirect("http://"+request.get_host()+"/file/explorer"+os.path.split(path)[0])