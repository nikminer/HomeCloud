from django.shortcuts import render,redirect
from django.http import HttpResponse
from .Common.directory import getPathHierrarhyFile
from .Common.movment import back
import base64
import shutil
import os
import time

def view1(request,path):    
    images=['WEBP','JPEG','SVG','PNG','GIF','JPG']
    texts= ['TXT','MB','LOG']
    if os.path.basename(path).split(".")[-1].upper() in images:
        return viewImage(request,path)
    elif os.path.basename(path).split(".")[-1].upper() in texts:
        return viewText(request,path)
    else:
        return back(request,path)

def deletefile(request,path):
    os.remove(path)
    return redirect("http://"+request.get_host()+"/file/back"+path)

def viewText(request, path):
    text = open(path,"r").read()
    return render(request, "File/TextFilePreview.html", 
    {       
        "filename":os.path.basename(path),
        "path":os.path.split(path)[0],
        "time":time.ctime(os.path.getctime(path)),
        "size":os.path.getsize(path),
        "text":text,
        "host":"http://"+request.get_host(),
        "pathes":getPathHierrarhyFile(path)
    })

def viewImage(request, path):
    image = open(path,"rb").read()
    base=str(base64.encodestring(image),"utf-8")
    
    return render(request, "File/ImageFilePreview.html", 
    {       
        "filename":os.path.basename(path),
        "path":os.path.split(path)[0],
        "time":time.ctime(os.path.getctime(path)),
        "size":os.path.getsize(path),
        "hash":base,
        "host":"http://"+request.get_host(),
        "pathes":getPathHierrarhyFile(path)
    })