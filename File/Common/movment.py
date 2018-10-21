from django.shortcuts import redirect,render
from .directory import isAccess,getPathHierrarhy
import shutil
import os

def back(request,path):
    print (os.path.split(path)[0])
    if path=="\\":
        redirect("http://"+request.get_host())
    else:
        return redirect("http://"+request.get_host()+"/file/explorer"+os.path.split(path)[0])

def explorer(request, path):
    DirList=[]
    FileList=[]
    path= os.path.splitdrive(os.path.expanduser(path).replace("\\","/"))[1]

    for i in os.listdir(path):
        if os.path.isdir(os.path.abspath(path+"\\"+i)) and isAccess(os.path.abspath(path+"\\"+i)):
            DirList.append(i)
        elif os.path.isfile(os.path.abspath(path+"\\"+i)) and os.access(os.path.abspath(path+"\\"+i),os.R_OK):
            FileList.append(i)

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

