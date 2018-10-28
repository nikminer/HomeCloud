from django.shortcuts import redirect
import shutil,os


def deletedir(request,path):
    shutil.rmtree(path)
    return redirect("http://"+request.get_host()+"/file/back"+path)

def createdir(request,path):
    os.mkdir(path)
    return redirect("http://"+request.get_host()+"/file/back"+path) 

def movedir(request,path,path1):
    os.replace(path+"/"+request.GET.get('name'),path1+"/"+request.GET.get('name'))
    return redirect("http://"+request.get_host()+"/file/explorer"+path1) 