from django.shortcuts import redirect
import shutil,os


def deletedir(request,path):
    shutil.rmtree(path)
    return redirect("http://"+request.get_host()+"/file/back"+path)

def createdir(request,path):
    os.mkdir(path)
    return redirect("http://"+request.get_host()+"/file/back"+path) 

def movedir(request):
    shutil.move(request.POST.get('originalpath'),request.POST.get('destionalpath'))
    return redirect("http://"+request.get_host()+"/file/explorer"+request.POST.get('destionalpath')) 

def deletefile(request,path):
    os.remove(path)
    return redirect("http://"+request.get_host()+"/file/back"+path)