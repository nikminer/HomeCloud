#подключаем модули
from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse,StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from File.models import Publicfile
import os
#Отправляем пользователю страницу публикации файла
@login_required
def Shering(request,path):
        return render(request, "Public/AddToPublic.html", 
        {
                'path':path,
                "host":request.scheme + "://" + request.get_host(),
        })
#Функция отвечает за переключение видимости публичного файла
@login_required
def SwithVisFile(request):
        #получаем публичный файл из бд
        userfile=Publicfile.objects.filter(Sharinguser=request.user).get(pseudoname=request.POST['ModalData'])
        #переключаем видимость
        userfile.isvisible=not userfile.isvisible== 'True'
        #сохраняем изменения и переходим обратно на страницу с файлами
        userfile.save()
        return HttpResponseRedirect("/file/public/share/getFiles")
#функция отвечает за удаление публичного файла из доступа
@login_required
def DelPubFile(request):
        #получение публичного файла и его последующее удаление
        Publicfile.objects.filter(Sharinguser=request.user).get(pseudoname=request.POST['ModalData']).delete()
        return HttpResponseRedirect("/file/public/share/getFiles")
#функция отвечает за отправку страницы со всеми файлами пользователя
@login_required
def GetUserFile(request):
        Uflies=[]
        #получаем все файлы пользователя
        for i in Publicfile.objects.filter(Sharinguser=request.user):
                try:
                        #пытаемся получить размер файла
                        size=os.path.getsize(i.path)
                except FileNotFoundError:
                        size=0
                #сохраняем публичный файл в объекте класса UserFile
                Uflies.append(UserFile(pn=i.pk,size=size,path=i.path,visible=i.isvisible))
        return render(request, "Public/UserFileList.html", 
        {
                "host":request.scheme + "://" +request.get_host(),
                "list":Uflies
        })
#данная функция проверяет доступен ли псевдоним
def exist(request):
        return HttpResponse(not Publicfile.objects.filter(pseudoname=request.POST['name']).count()>0)
#Данная функция отвечает за добовление файла в бд
@login_required
def AddFile(request):
        Publicfile.objects.create(pseudoname=request.POST['name'],path=request.POST['path'],Sharinguser=request.user.username,isvisible='isVisible' in request.POST.keys()).save()
        return HttpResponseRedirect("/file/public/")
#Данная функция отвечает за скачивание публичного файла
def download(request,name):
        #данная функция в функцие перебирает ассинхрнно возвращает поток с файлом
        def file_iterator(file_name, chunk_size=512):
                #открываем файл для чтения побайтово
                with open(file_name,'rb') as f:
                        while True:
                                #в бесконечном цикле читаем чанк
                                chunk = f.read(chunk_size)
                                if chunk:
                                        #ассинхронно возврщаем чанк
                                        yield chunk
                                else:
                                        break
        #получаем путь к файлу
        path= Publicfile.objects.get(pseudoname=name).path
        #создаём потоковый ответ на запрос
        response = StreamingHttpResponse(file_iterator(path))
        response['Content-Type'] = 'application/octet-stream'
        #возвращаем поток
        response['Content-Disposition'] = 'attachment;filename="{0}{1}"'.format(name,os.path.splitext(path)[1])
        return response
#фукция отвечает за возвращение страницы с публичными файлами на сервере
def explorePublic(request):
        Pflies=[]
        #получаем все видимые публичные файлы
        for i in Publicfile.objects.filter(isvisible="True"):
                try:
                        #получаем всю возможную информацию о файле
                        Pflies.append(Public(pn=i.pk,user=i.Sharinguser,size=os.path.getsize(i.path)))
                except FileNotFoundError:
                        #если файл отсутсвует в файловой системе, то удаляем запись о нём
                        Publicfile.objects.get(pseudoname=i.pk).delete()

        return render(request, "Public/PublicList.html", 
        {
                "host":request.scheme + "://" +request.get_host(),
                "list":Pflies
        })
#Данный модуль отвечает за хранение и отправку данных о публичном файле
class Public:
        pn=""
        size=0
        user=""
        def __init__(self, pn,size,user):
                self.pn=pn
                self.size=size
                self.user=user
#Данный модуль отвечает за хранение и отправку данных о публичном файле пользователя
class UserFile:
        pn=""
        size=0
        visible=True
        path=""
        def __init__(self, pn, size,path, visible):
                self.pn=pn
                self.size=size
                self.path=path
                self.visible=visible
        