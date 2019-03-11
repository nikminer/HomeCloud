import os
import zipfile
from django.http import StreamingHttpResponse
from .directory import isAccess

def downloadFile(request, path):
    
    def file_iterator(file_name, chunk_size=512):
        with open(file_name,'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if chunk:
                    yield chunk
                else:
                    break

    response = StreamingHttpResponse(file_iterator(path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(os.path.split(path)[1])
    return response

def downloadFolder(request,path):
    pathes=os.path.split(path)

    zipf = zipfile.ZipFile(path+"/"+pathes[1]+".zip", 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            if(file != pathes[1]+".zip"):
                absfn=os.path.join(root, file)
                zfn = absfn[len(path)+len(os.sep):]
                try:
                    zipf.write(absfn,zfn)
                except PermissionError:
                    pass
    zipf.close()

    def dir_iterator(file_name, chunk_size=512):
        with open(file_name,'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if chunk:
                    yield chunk
                else:
                    f.close()
                    os.remove(file_name)
                    break

    response = StreamingHttpResponse(dir_iterator(path+"/"+pathes[1]+".zip"))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(pathes[1]+".zip")
    return response