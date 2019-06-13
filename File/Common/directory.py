#подключаем модуль для взаимодействия с БД
import os
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#функция отвечающая за проверку доступности директории
def isAccess(path):
    try:
        #пробуем получить список файлов в директории
        os.listdir(path)
        #если у нас получается, то возвращаем истину
        return True
    except PermissionError:
        #если водникает исключения ощибка доступа, то возвращаем ложь
        return False
#функция отвечает существет ли файл по определённому пути, необходима для праверки наличия папки при создание новой папки
@login_required
def isExist(request):
    return HttpResponse(os.path.exists(os.path.abspath(request.POST['path'])))
#функция отвечает за возврат иерархии путей
def getPathHierrarhy(fullPath):
    #создаём лист для хранения путей
    pathes=[]
    #хранит путь по которому мы проходимся
    currpath=""
    if fullPath:
        #перебираем полученный путь который мы поделили на множество частей
        for dir in fullPath[1:].split("/"):
            #создаём объект класса Path
            path=Path()
            #присваивание  объекту название папки
            path.dir=dir
            #добавляем к текущему пути директорию
            currpath+=dir
            #присваивание  объекту путь к папке
            path.hierrarhy=currpath
            #добпаляем путь в массив с путями
            pathes.append(path)
            #отделяем следующую директорию
            currpath+="/"
        #возвращаем иеррарзию путей
        return pathes
#функция отвечает за возврат иерархии пути к файлу
def getPathHierrarhyFile(fullPath):
    pathes=[]
    currpath=""
    if fullPath:
        for dir in fullPath[1:].split("/"):
            path=Path()
            path.dir=dir
            currpath+=dir
            path.hierrarhy=currpath
            pathes.append(path)
            currpath+="/"
        #но тут  лишь удаляется последний путь содержащее имя файла
        del pathes[-1]
        return pathes
#класс для иеррархии путей
class Path:
    dir=""
    hierrarhy=""