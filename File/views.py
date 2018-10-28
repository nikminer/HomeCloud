from django.shortcuts import render,redirect
from django.http import HttpResponse
import base64
import shutil
import os


def view1(request, path):
    image = open(path,"rb").read()
    base=str(base64.encodestring(image),"utf-8")
    
    return render(request, "File/filePreview.html", 
    {   
        "hash":base,
        "host":"http://"+request.get_host()+"/file",
    })

