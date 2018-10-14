from django.shortcuts import render,redirect
from django.http import HttpResponse

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
        "host":"http://"+request.get_host()+"/file"
    })

def isAccess(path):
    try:
        os.listdir(path)
        return True
    except PermissionError:
        return False

def back(request,path):
    print (os.path.split(path)[0])
    if path=="\\":
        redirect("http://"+request.get_host())
    else:
        return redirect("http://"+request.get_host()+"/file/explorer"+os.path.split(path)[0])