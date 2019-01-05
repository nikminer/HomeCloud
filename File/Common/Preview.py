import base64
import os
import time
from django.shortcuts import render
from .directory import getPathHierrarhyFile
import json

conf=json.loads(open("static/config/Groups.json","r").read())
images=[]
texts= []

for i in conf:
    if conf[i]['type']=="pic":
        images.extend(conf[i]['formats'])
    if conf[i]['type']=="text":
        texts.extend(conf[i]['formats'])

def ViewSwitcher(request,path):
    if os.path.basename(path).split(".")[-1].upper() in images:
        return PreviewImage(request,path)
    elif os.path.basename(path).split(".")[-1].upper() in texts:
        return PreviewText(request,path)
    else:
        return render(request, "File/FilePreview.html", 
        {       
            "filename":os.path.basename(path),
            "path":os.path.split(path)[0],
            "time":time.ctime(os.path.getctime(path)),
            "size":os.path.getsize(path),
            "host":"http://"+request.get_host(),
            "pathes":getPathHierrarhyFile(path)
        })

def PreviewText(request, path):
    text = open(path,"r",encoding='utf-8').read()

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

def PreviewImage(request, path):
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