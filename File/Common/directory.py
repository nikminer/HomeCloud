import os
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def isAccess(path):
    try:
        os.listdir(path)
        return True
    except PermissionError:
        return False
@login_required
def isExist(request,path):
    return HttpResponse(os.path.exists(os.path.abspath(path)))

def getPathHierrarhy(fullPath):
    pathes=[]
    currpath=""
    if fullPath:
        for dir in fullPath[1:].split("/"):
            path=Path()
            path.dir=dir
            currpath+=dir+"/"
            path.hierrarhy=currpath
            pathes.append(path)
            pathes[-1].hierrarhy=pathes[-1].hierrarhy[0:-1]
        return pathes

def getPathHierrarhyFile(fullPath):
    pathes=[]
    currpath=""
    if fullPath:
        for dir in fullPath[1:].split("/"):
            path=Path()
            path.dir=dir
            currpath+=dir+"/"
            path.hierrarhy=currpath
            pathes.append(path)
            pathes[-1].hierrarhy=pathes[-1].hierrarhy[0:-1]
        del pathes[-1]
        
        return pathes

class Path:
    dir=""
    hierrarhy=""