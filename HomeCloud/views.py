#подключаем необходимые модули
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
import psutil,os,platform
import shutil
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib.auth.models import User
from File.models import Publicfile
#Возвращаем страницу аунтентификации
def getlogin(request):
    return render(request,'HomeCloud/auth.html',{"next":request.GET['next']})
#Возвращаем страницу настройки пользователей
@login_required
def Users(request):
    #проверяем права пользователя
    if request.user.is_superuser:
        return render(request,'HomeCloud/Settings/Users.html',{
            'users':User.objects.all() #запращиваем всех пользователей из БД
        })
    else:   
        #Если не админ делает запрос то возвращаем его на главную страницу
        return redirect('../..')
#Возвращаем страницу создания нового пользователя
@login_required
def CreateUser(request):
    #проверяем права пользователя
    if request.user.is_superuser:
        return render(request,'HomeCloud/Settings/create.html')
    else:   
        #Если не админ делает запрос то возвращаем его на главную страницу
        return redirect('../..')
#Создаём нового пользователя
@login_required
def Save(request):
    #проверяем права пользователя
    if request.user.is_superuser:
        #Заносим пользователя в БД
        User.objects.create_user(username=request.POST['username'],password=request.POST['pass'])
        #Создаём для него папку
        os.mkdir(os.path.expanduser("~/"+request.POST['username']))
        #Перекидываем админа на страницу со всеми пользователями
        return redirect(".")
    #Если не админ делает запрос то возвращаем его на главную страницу
    else:   
        return redirect('../..')
#Удаляем пользователя
@login_required
def DeleteUser(request,user):
    #проверяем права пользователя
    if request.user.is_superuser:
        u = User.objects.get(username = user)#запращиваем пользователя из БД
        u.delete()#удаляем его
        #запращиваем все публичные файлы пользователя и удаляем их тоже
        for i in Publicfile.objects.filter(Sharinguser=user):
            i.delete()
        #проверяем существует ли папка пользователя, если да то удаляем её
        if os.path.exists(os.path.expanduser("~/"+user)):
            shutil.rmtree(os.path.expanduser("~/"+user))
        #Перекидываем админа на страницу со всеми пользователями
        return redirect(".")
    #Если не админ делает запрос то возвращаем его на главную страницу
    else:   
        return redirect('../..')
#производим аутентификацию пользовавателя
def login(request):
    #запращиваем данные
    user = auth.authenticate(username=request.POST['login'], password=request.POST['pass'])
    #если пользователь существует и он активен
    if user is not None and user.is_active:
        #производим аутентификацию
        auth.login(request, user)
        #перебрасываем на страницу из пост запроса
        return HttpResponseRedirect(request.POST['next'])
    #иначе возвращаемся на страницу аутентификции
    else:
        return HttpResponseRedirect("/accounts/login?next="+request.POST['next'])
#выход из аккаунта пользователя
@login_required
def logout(request):
    #выходим из аккаунта пользователя
    auth.logout(request)
    #возвращаемся на страницу аутентификции
    return HttpResponseRedirect("/accounts/login/?next=/")

#конвертер байтов
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
#возврат загруженности процессора
@login_required
def getCPUpercent(request):
    return HttpResponse(psutil.cpu_percent(interval=1))
#возврат загруженности ОП
@login_required
def getVirtualmemory(request):
    return HttpResponse(DiskSize(psutil.virtual_memory().free,psutil.virtual_memory().used,psutil.virtual_memory().total).percent)
#возврат загруженности Файла подкачки
@login_required
def getSwapmemory(request):
    return HttpResponse(DiskSize(psutil.swap_memory().free,psutil.swap_memory().used,psutil.swap_memory().total).percent)
#Класс для хранения и отправки значений связанных с размером чего нибыло
class DiskSize:
    used=0
    free=0
    total=0
    percent=0
    def __init__(self,free,used,total):
            self.free=free
            self.used=used
            self.total=total
            self.percent=round(used/(total/100),1)
#возврат размеров жёсткого диска
def getDiskspace():
    return DiskSize(shutil.disk_usage("/").free,shutil.disk_usage("/").used,shutil.disk_usage("/").total)
#возврат размеров ОП
def Virtualmemory():
    return DiskSize(psutil.virtual_memory().free,psutil.virtual_memory().used,psutil.virtual_memory().total)
#возврат размеров Файла подкачки
def Swapmemory():
    return DiskSize(psutil.swap_memory().free,psutil.swap_memory().used,psutil.swap_memory().total)

#страница админа
@login_required
def admin(request):
    #проверяем права пользователя
    if request.user.is_superuser:
        iflist={}
        #получение списка сетевых подключений
        for i in psutil.net_if_addrs():
            iflist[i]=[]
            for i1 in psutil.net_if_addrs()[i]:
                iflist[i].append({"address":i1.address,"netmask":i1.netmask,"broadcast":i1.broadcast})
        import multiprocessing
        #список данные о системе
        DataList={
            "osname":platform.system()+" "+platform.release(),
            "Node":platform.node(),
            "CPUname":platform.processor(),
            "CPUcount":multiprocessing.cpu_count(),
            "diskspace":getDiskspace(),
            "VMspace":Virtualmemory(),
            "SMspace":Swapmemory(),
            "bytesent":psutil.net_io_counters().bytes_sent,
            "byterecv":psutil.net_io_counters().bytes_recv,
            "packsent":psutil.net_io_counters().packets_sent,
            "packrecv":psutil.net_io_counters().packets_recv,
            "iflist":iflist,
        }
        #проверка на загруженность диска
        if round(shutil.disk_usage('.').free/1073741824,3)<10:
            DataList['Sysproblem']=ugettext("Free disk space less 10 GB")
        return render(request,'HomeCloud/admin.html',DataList)
    #иначе возвращаемся на страницу аутентификции
    else:   
        return redirect('..')

#отправка главной страницы 
@login_required
def index(request):
    return render(request,'HomeCloud/index.html',{
        "diskspace":getDiskspace(),
    })
#отправка страницы со сменой пароля и механизм смены пароля
@login_required
def CHPass(request):
    #проверка на наличее данных POST-запроса
    if not request.POST:
        return render(request, "HomeCloud/Settings/ChangePassword.html", {'form':PasswordChangeForm(user=request.user)})
    #иначе проверяем форму и меняем пароль
    else:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        #если форма валидна, то меняем пароль
        if form.is_valid():   
            form.save()
            #разлогиниваемся
            auth.logout(request)
            #переходим на страницу авторизации
            return HttpResponseRedirect("/accounts/login/?next=/")
        #иначе возвращаемся на форму смены пароля
        else:
            return render(request, "HomeCloud/Settings/ChangePassword.html", {'form':form})
#данная функция аналочично функции смены пароля, только эта устанваливет пароль и проверяет наличие права администратора
@login_required
def SetPass(request,user):
    if request.user.is_superuser:
        if not request.POST:
            return render(request, "HomeCloud/Settings/setpassword.html", {'form':SetPasswordForm(user=User.objects.get(username = user))})
        else:
            form = SetPasswordForm(user=User.objects.get(username = user), data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/admin/Users/")
            else:
                return render(request, "HomeCloud/Settings/setpassword.html", {'form':form})
    else:   
        return redirect('..')   
    