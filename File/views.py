from django.shortcuts import render,redirect
from django.http import HttpResponse
from .Common.directory import getPathHierrarhyFile
from .Common.movment import back
import base64
import shutil
import os
import time

def convertBytes(byte):
    if byte>1024 and byte<1048575:
        return str(round(byte/1024,3))+ " KB"
    elif byte>1048576 and byte<1073741823:
        return str(round(byte/1048576,3))+ " MB"
    elif byte>1073741824 and byte<1099511627775:
        return str(round(byte/1073741824,3)) + " GB"
    elif byte>1099511627776:
        return str(round(byte/1099511627776))+" PB"
    return str(byte) + " Bytes"

def view1(request,path):    
    images=['WEBP','JPEG','SVG','PNG','GIF','JPG']

    if os.path.basename(path).split(".")[-1].upper() in images:
        return viewImage(request,path)
    else:
        return back(request,path)

def viewImage(request, path):
    image = open(path,"rb").read()
    base=str(base64.encodestring(image),"utf-8")
    
    return render(request, "File/filePreview.html", 
    {       
        "filename":os.path.basename(path),
        "path":os.path.split(path)[0],
        "time":time.ctime(os.path.getctime(path)),
        "size":convertBytes(os.path.getsize(path)),
        "hash":base,
        "host":"http://"+request.get_host(),
        "pathes":getPathHierrarhyFile(path)
    })