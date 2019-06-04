from django.shortcuts import render,redirect
import json
from .movment import Groupe
from ..forms import UploadIconForm
from django.contrib.auth.decorators import login_required
from .uploads import handle_uploaded_file_WITHNAME
import os
import shutil

@login_required
def Groups(request):
	conf=json.loads(open("static/File/config/Groups.json","r").read())
	groups=[]
	for i in conf:
		groups.append(Groupe(i,conf[i]['icon']))
	return render(request, "Settings/Settings.html", 
	{
		'config':groups
	})

@login_required
def DeleteGroup(request,group):
	conf=json.loads(open("static/File/config/Groups.json","r").read())
	
	os.remove("static/"+conf[group]['icon'])
	conf.pop(group)
	open("static/File/config/Groups.json","w").write(json.dumps(conf))
	return redirect('../groups')

@login_required
def EditGroup(request,group=None):
	if group:
		conf=json.loads(open("static/File/config/Groups.json","r").read())

		return render(request, "Settings/Edit.html", 
		{
			'name':group,
			'icon':conf[group]['icon'],
			'formats':conf[group]['formats'],
			'type':conf[group]['type'],
			'forms':UploadIconForm()
		})
	else:
		return render(request, "Settings/Edit.html", {'forms':UploadIconForm()})

@login_required
def Save(request):
	conf=json.loads(open("static/File/config/Groups.json","r").read())
	dic={
		"formats":json.loads(request.POST['formatlists']),
		"type":request.POST['type']
	}
	icon=None
	if not 'Icon' in request.POST:
		form = UploadIconForm(request.POST, request.FILES)
		if form.is_valid():
			filename=request.POST['groupname']+"."+request.FILES['Icon'].name.split('.')[-1]
			handle_uploaded_file_WITHNAME(request.FILES['Icon'],"static/File/images/Groups/"+filename,request)
			icon="File/images/Groups/"+filename

	if request.POST['firstname'] in conf:
		if not icon: icon=conf[request.POST['firstname']]['icon']
		if (request.POST['groupname']!=request.POST['firstname']):
			conf.pop(request.POST['firstname'])
	else:
		if not icon :
			shutil.copyfile("static/File/images/Groups/file.png","static/File/images/Groups/"+request.POST['groupname']+".png")
			icon="File/images/Groups/"+request.POST['groupname']+".png"
	
	dic['icon']=icon
	conf[request.POST['groupname']]=dic
	open("static/File/config/Groups.json","w").write(json.dumps(conf))
	return redirect('../groups')