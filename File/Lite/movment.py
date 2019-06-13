#подключаем модули
from django.http import HttpResponse
import os
import json
from File.Common.directory import isAccess
from django.contrib.auth.decorators import login_required
#функция отвечает за легковесную отправку всех директорий
@login_required
def explorerDir(request, path):
    #обрабатываем путь
    path= os.path.splitdrive(os.path.expanduser(path).replace('\\','/'))[1]
    dirs=[]
    #перебираем всё содержимое директории
    for i in os.listdir(path):
        #если элемент текущей директории - это директория, то добавляем в список
        if os.path.isdir(os.path.abspath(path+"/"+i)) and isAccess(os.path.abspath(path+"/"+i)):
            dirs.append(i)
    #возвращаем ответ
    return HttpResponse(json.dumps(dirs))

#функция отвечает за легковесную отправку всех файлов, аналогично легковесной отправки директории
@login_required
def explorerFiles(request, path):
    path= os.path.splitdrive(os.path.expanduser(path).replace('\\','/'))[1]
    files=[]
    for i in os.listdir(path):
        if os.path.isfile(os.path.abspath(path+"/"+i)):
            files.append(i)
    return HttpResponse(json.dumps(files))