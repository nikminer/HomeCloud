#подключаем модули
import base64
import os
import time
from django.shortcuts import render
from .directory import getPathHierrarhyFile
import json
from PIL import Image
import io
import codecs
from django.contrib.auth.decorators import login_required
#функция отвечает за определение типа файла и его открытие в нужном виде
@login_required
def ViewSwitcher(request,path):
    #получаем конфигурацию групп
    conf=json.loads(open("static/File/config/Groups.json","r").read())
    images=[]
    texts= []
    #перебираем группы и сортируем расширение по типу файла
    for i in conf:
        if conf[i]['type']=="pic":
            images.extend(conf[i]['formats'])
        if conf[i]['type']=="text":
            texts.extend(conf[i]['formats'])
    #если расширение файла совпадает с картинкми то отображаем страницу с этой картинкой
    if os.path.basename(path).split(".")[-1].upper() in images:
        return PreviewImage(request,path)
    #иначе проверяем расширение файла подходит ли он по типу с текстовой информацией, если да то отображаем страницу с содержимым файла
    elif os.path.basename(path).split(".")[-1].upper() in texts:
        return PreviewText(request,path)
    #иначе отображаем страницу с базовой информацией о файле
    else:
        return render(request, "File/FilePreview.html", 
        {       
            "filename":os.path.basename(path),
            "path":os.path.split(path)[0],
            "time":time.ctime(os.path.getctime(path)),
            "size":os.path.getsize(path),
            "host":request.scheme + "://" +request.get_host(),
            "pathes":getPathHierrarhyFile(path)
        })
#функция отвечает за отображения файла с текстовой информацией
@login_required
def PreviewText(request, path):
    #чтение содержимого файла
    text= codecs.open(path, 'r', encoding='utf-8',errors='ignore').read()
    return render(request, "File/TextFilePreview.html", 
    {       
        "filename":os.path.basename(path),
        "path":os.path.split(path)[0],
        "time":time.ctime(os.path.getctime(path)),
        "size":os.path.getsize(path),
        "text":text,
        "host":request.scheme + "://" +request.get_host(),
        "pathes":getPathHierrarhyFile(path)
    })
#функция отвечает за отображения файла с графической информацией
@login_required
def PreviewImage(request, path):
    #побайтовое чтение файла
    image = open(path,"rb").read()
    #хеширование в base64
    base=str(base64.encodestring(image),"utf-8")
    return render(request, "File/ImageFilePreview.html", 
    {       
        "filename":os.path.basename(path),
        "path":os.path.split(path)[0],
        "time":time.ctime(os.path.getctime(path)),
        "size":os.path.getsize(path),
        "hash":base,
        "host":request.scheme + "://" +request.get_host(),
        "pathes":getPathHierrarhyFile(path)
    })
#фуникция отвечает за превью картинок в файловом обозревателе
def GetCode(path):
    #открываем картинку
    img= Image.open(path)
    #вырезаем центр из картинки.
    if (img.size[0]>img.size[1]):
        newwidth=round(img.size[0]/2)  
        cimg=img.crop((round(newwidth*0.5),0,round(newwidth*1.5),round(img.size[1]*0.7)))
    else:
        newwidth=round(img.size[0]/2) 
        newheight=round(img.size[1]/2)  
        cimg=img.crop((round(newwidth*0.7),round(newheight*0.7),round(newwidth*1.5),round(newheight*1.5)))
    #ресайзим картинку до размера 45px
    cimg=cimg.resize((45,45))
    #отправляем захешированную картинку
    in_mem_file = io.BytesIO()
    cimg.save(in_mem_file, format = img.format)
    in_mem_file.seek(0)
    img_bytes = in_mem_file.read()
    code = base64.b64encode(img_bytes).decode('ascii')
    return "data:image/"+str(img.format)+";base64,"+code
