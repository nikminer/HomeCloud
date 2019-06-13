#подключаем модули
from django.shortcuts import redirect,render
from .directory import isAccess,getPathHierrarhy
from HomeCloud.views import getDiskspace
from ..forms import UploadFileForm
from .uploads import handle_uploaded_file
from .Preview import GetCode
import shutil
import os
import json
import datetime
from django.contrib.auth.decorators import login_required
#функция отвечающая за загрузку файла на сервер
@login_required
def upload_file(request):
    #проверка на отправку файлов
    if request.method == 'POST':
        #получаем форму с отправленным на сервере файлом
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #перебираем файлы
            for f in form.files.getlist('File'):
                #потоковая загрузка файла на сервер
                handle_uploaded_file(f,request.POST['path'],request)
            return redirect(request.scheme + "://" +request.get_host()+"/file/explorer"+request.POST['path'])
    explorer(request,request.POST['path'])
#функция отвечающая за переход в родительскую директорию
@login_required
def back(request,path):
    if path=="/":
        redirect(request.scheme + "://" +request.get_host())
    else:
        return redirect(request.scheme + "://" +request.get_host()+"/file/explorer"+os.path.split(path)[0])
#функция отвечающая за переход в директорию по ссылке
@login_required
def explorer(request, path):
    #получаем конфигурацию групп
    conf=json.loads(open("static/File/config/Groups.json","r").read())
    #список директорий
    DirList=[]
    #списко файлов
    FileList=Files()
    #очередь группы
    GroupQueue={}
    QueueIndex=0
    #путь к домащней директории системы
    replacment=os.path.splitdrive(os.path.expanduser('~'))[1].replace('\\','/')
    #проверка привилегий пользовтеля
    if not request.user.is_superuser:
        replacment+="/"+request.user.username
    #замена ~ на путь к домашней директории пользователя
    path= os.path.splitdrive(path.replace("~",replacment).replace('\\','/'))[1]
    #проверка на путь к директории и возврат на главную, если пользователь переходит куда не следует
    if not request.user.is_superuser and not replacment in path:
        return redirect(request.scheme + "://" +request.get_host())
    #перебор конфигураций групп
    for i in conf:
        #перебор форматов файла в конфигурации с занесением в список файлов
        for i1 in conf[i]['formats']:
            FileList.formats.update({i1:i})
        #добавление пути к иконке в объект класса FileList
        FileList.groups.append(Groupe(i,conf[i]['icon']))
        #добавление группы в очередь
        GroupQueue.update({i:QueueIndex})
        QueueIndex+=1
    #добавление группы "прочее" для файлов не имеющих своей группы
    FileList.groups.append(Groupe("Others","File/images/file.png"))
    GroupQueue.update({"Other":QueueIndex})
    #перебор файлов в директории по пути path
    for i in os.listdir(path):
        if path=="/":
            path=""
        #проверка на директория ли это и достпна ли она
        if os.path.isdir(os.path.abspath(path+"/"+i)) and isAccess(os.path.abspath(path+"/"+i)):
            #если да то добавление директории как объект класса Directory в список
            DirList.append(Dirictory(i,os.path.getctime(path+"/"+i)))
        #иначе проверка на файл доступность файла
        elif os.path.isfile(os.path.abspath(path+"/"+i)) and os.access(os.path.abspath(path+"/"+i),os.R_OK):
            #поулчение группы файла по его расширению
            i1=FileList.formats.get(i.split(".")[-1].upper())
            #если есть группа у файла то группируем файл в списке файлов
            if i1:
                if (i1=="Pictures"):
                    FileList.groups[GroupQueue[i1]].list.append(Image(i,os.path.getsize(path+"/"+i),os.path.getctime(path+"/"+i),GetCode(path+"/"+i)))
                else:
                    FileList.groups[GroupQueue[i1]].list.append(fileobj(i,os.path.getsize(path+"/"+i),os.path.getctime(path+"/"+i)))
            #иначе заносим файл в папку прочее
            else:
                FileList.groups[GroupQueue["Other"]].list.append(fileobj(i,os.path.getsize(path+"/"+i),os.path.getctime(path+"/"+i)))
    #возвращаем пользователю обозреватель директории
    return render(request, "File/explorer.html", 
    {
        "dirs": DirList,
        "disk":getDiskspace,
        "files":FileList,
        "path":path,
        "host":request.scheme + "://" +request.get_host(),
        "pathes":getPathHierrarhy(path),
        "forms":UploadFileForm()
    })
#класс для хранения файлов
class Files:
    groups=[]
    formats={}
    def __init__(self):
        self.groups=[]
        self.formats={}
#класс для хранения и передачи директорий
class Dirictory:
    name=""
    date=""
    def __init__(self,name,date):
        self.name=name
        self.date= datetime.date.fromtimestamp(date)
#класс для хранения и передачи групп
class Groupe(object):
    name=""
    icon=""
    list=[]
    def __init__(self,name,icon):
        self.name=name
        self.list=[]
        self.icon=icon
#класс для хранения файлов
class fileobj(object):
    name=""
    size=0
    date=""
    def __init__(self,name,size,date):
        self.name=name
        self.size=size
        self.date= datetime.date.fromtimestamp(date)
#класс для хранений изображений, наследующий от класса fileobj
class Image(fileobj):
    code=""
    def __init__(self,name,size,date,code):
        super().__init__(name,size,date)
        self.code=code
        