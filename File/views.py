from django.shortcuts import render,redirect

import os
from django.http import StreamingHttpResponse

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