from django.shortcuts import redirect
import shutil,os
import json
from django.contrib.auth.decorators import login_required
@login_required
def deletedir(request):
	shutil.rmtree(request.POST['delpath'])
	return redirect(request.scheme + "://" +request.get_host()+"/file/back"+request.POST['delpath'])
@login_required
def createdir(request):
	print(request.POST)
	path=request.POST['dirpath']+request.POST['path']
	os.mkdir(path)
	return redirect(request.scheme + "://" +request.get_host()+"/file/back"+path) 
@login_required
def movedir(request):
    shutil.move(request.POST.get('originalpath'),request.POST.get('destionalpath'))
    return redirect(request.scheme + "://" +request.get_host()+"/file/explorer"+request.POST.get('destionalpath')) 
@login_required
def deletefile(request):
    os.remove(request.POST['delpath'])
    return redirect(request.scheme + "://" +request.get_host()+"/file/back"+request.POST['delpath'])

@login_required
def delete(request):
	listF=json.loads(request.POST['list'])
	path=request.POST['delpath']
	for i in listF:
		if os.path.isdir(path+"/"+i):
			shutil.rmtree(path+"/"+i)
		else:
			os.remove(path+"/"+i)
	return redirect(request.scheme + "://" +request.get_host()+"/file/explorer"+path)