from django.http import HttpResponse
import os
import json

from File.Common.directory import isAccess


from django.contrib.auth.decorators import login_required

@login_required
def explorerDir(request, path):
    path= os.path.splitdrive(os.path.expanduser(path).replace('\\','/'))[1]
    dirs=[]
    for i in os.listdir(path):
        if os.path.isdir(os.path.abspath(path+"/"+i)) and isAccess(os.path.abspath(path+"/"+i)):
            dirs.append(i)
    return HttpResponse(json.dumps(dirs))