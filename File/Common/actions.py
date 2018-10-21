from django.shortcuts import redirect
import shutil


def deletedir(request,path):
    shutil.rmtree(path)
    return redirect("http://"+request.get_host()+"/file/back"+path)