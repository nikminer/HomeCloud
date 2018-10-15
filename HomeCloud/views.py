from django.shortcuts import render
from django.http import HttpResponse
import psutil,os,platform


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

def getCPUpercent(request):
    return HttpResponse(psutil.cpu_percent(interval=1))

def disk_usage(path):
    total=0
    used=0
    free=0
    if os.name == "posix":
        info = os.statvfs(path)
        total = info.f_blocks * info.f_frsize
        free = info.f_bavail * info.f_frsize
        used = total - free
    elif os.name=="nt":
        #from . import _psutil_windows as psutil
        total= psutil.disk_usage(path).total
        free= psutil.disk_usage(path).free
        used = total - free
    return {'total':total, 'used':used, 'free':free}

def index(request):
    iflist={}
    for i in psutil.net_if_addrs():
        iflist[i]=[]
        for i1 in psutil.net_if_addrs()[i]:
            iflist[i].append({"address":i1.address,"netmask":i1.netmask,"broadcast":i1.broadcast})
    DataList={
        "osname":platform.system()+" "+platform.release(),
        "Node":platform.node(),
        "CPUname":platform.processor(),
        "CPUcount":psutil.cpu_count(logical=False),
        "freespace":round(disk_usage('.')['free']/1073741824,3),
        "usedspace":round(disk_usage('.')['used']/1073741824,3),
        "totalspace":round(disk_usage('.')['total']/1073741824,3),
        "VMfreespace":round(psutil.virtual_memory().free/1073741824,3),
        "VMusedspace":round(psutil.virtual_memory().used/1073741824,3),
        "VMtotalspace":round(psutil.virtual_memory().total/1073741824,3),
        "SMfreespace":round(psutil.swap_memory().free/1073741824,3),
        "SMusedspace":round(psutil.swap_memory().used/1073741824,3),
        "SMtotalspace":round(psutil.swap_memory().total/1073741824,3),
        "bytesent":convertBytes(psutil.net_io_counters().bytes_sent),
        "byterecv":convertBytes(psutil.net_io_counters().bytes_recv),
        "packsent":psutil.net_io_counters().packets_sent,
        "packrecv":psutil.net_io_counters().packets_recv,
        "iflist":iflist
    }
    if round(disk_usage('.')['free']/1073741824,3)<10:
        DataList['Sysproblem']="Free disk space less 10 GB"
    return render(request,'HomeCloud/index.html',DataList)
