import os
import zipfile
from django.http import StreamingHttpResponse, FileResponse
from .directory import isAccess
from django.contrib.auth.decorators import login_required
import json

@login_required
def downloadFile(request, path):
    response = FileResponse(open(path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(os.path.split(path)[1])
    return response

@login_required
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
	fname=pathes[1]+".zip"
	return SendFile(path+"/"+fname,fname)

@login_required
def download(self,path,listf):
	print(path,listf)
	pathes=os.path.split(path)
	Files=json.loads(listf)
	if Files:
		zipf = zipfile.ZipFile(path+"/"+pathes[1]+".zip", 'w', zipfile.ZIP_DEFLATED)
		for i in Files:
			if os.path.isdir(path+"/"+i):
				absfn=os.path.join(path,i)
				zipf.write(absfn,i)
				for root, dirs, files in os.walk(path+"/"+i):
					for file in files:
						abspath=os.path.join(root, file)
						try:
							zipf.write(abspath,os.path.relpath(abspath,start=path))
						except PermissionError:
							pass
			else:
				absfn=os.path.join(path,i)
				zipf.write(absfn,i)
		zipf.close()
		fname=pathes[1]+".zip"
		return SendFile(path+"/"+fname,fname)

def SendFile(path,fname):
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
	response = StreamingHttpResponse(dir_iterator(path))
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fname)
	return response