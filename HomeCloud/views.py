from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import psutil,os,platform
import shutil
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.utils.translation import ugettext



def getlogin(request):
    return render(request,'HomeCloud/auth.html',{"next":request.GET['next']})

def login(request):
    user = auth.authenticate(username=request.POST['login'], password=request.POST['pass'])
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect(request.POST['next'])
    else:
        return HttpResponseRedirect("/accounts/login?next="+request.POST['next'])

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/?next=/")

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
@login_required
def getCPUpercent(request):
    return HttpResponse(psutil.cpu_percent(interval=1))
@login_required
def getVirtualmemory(request):
    return HttpResponse(DiskSize(psutil.virtual_memory().free,psutil.virtual_memory().used,psutil.virtual_memory().total).percent)
@login_required
def getSwapmemory(request):
    return HttpResponse(DiskSize(psutil.swap_memory().free,psutil.swap_memory().used,psutil.swap_memory().total).percent)

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

def getDiskspace():
    return DiskSize(shutil.disk_usage("/").free,shutil.disk_usage("/").used,shutil.disk_usage("/").total)
def Virtualmemory():
    return DiskSize(psutil.virtual_memory().free,psutil.virtual_memory().used,psutil.virtual_memory().total)
def Swapmemory():
    return DiskSize(psutil.swap_memory().free,psutil.swap_memory().used,psutil.swap_memory().total)

@login_required
def index(request):
    iflist={}
    for i in psutil.net_if_addrs():
        iflist[i]=[]
        for i1 in psutil.net_if_addrs()[i]:
            iflist[i].append({"address":i1.address,"netmask":i1.netmask,"broadcast":i1.broadcast})
    import multiprocessing
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
    if round(shutil.disk_usage('.').free/1073741824,3)<10:
        DataList['Sysproblem']=ugettext("Free disk space less 10 GB")
    return render(request,'HomeCloud/index.html',DataList)
