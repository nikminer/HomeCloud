from django.shortcuts import render
from django.http import HttpResponse
import psutil,os,platform
import shutil


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
        "freespace":round(shutil.disk_usage("/").free/1073741824,3),
        "usedspace":round(shutil.disk_usage("/").used/1073741824,3),
        "totalspace":round(shutil.disk_usage("/").total/1073741824,3),
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
    if round(shutil.disk_usage('.').free/1073741824,3)<10:
        DataList['Sysproblem']="Free disk space less 10 GB"
    return render(request,'HomeCloud/index.html',DataList)
