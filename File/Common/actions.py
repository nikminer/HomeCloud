from django.shortcuts import redirect
import shutil,os
from django.contrib.auth.decorators import login_required
@login_required
def deletedir(request,path):
    shutil.rmtree(path)
    return redirect("http://"+request.get_host()+"/file/back"+path)
@login_required
def createdir(request,path):
    os.mkdir(path)
    return redirect("http://"+request.get_host()+"/file/back"+path) 
@login_required
def movedir(request):
    shutil.move(request.POST.get('originalpath'),request.POST.get('destionalpath'))
    return redirect("http://"+request.get_host()+"/file/explorer"+request.POST.get('destionalpath')) 
@login_required
def deletefile(request,path):
    os.remove(path)
    return redirect("http://"+request.get_host()+"/file/back"+path)