from django.shortcuts import render,redirect
import json
from .movment import Groupe
from ..forms import UploadIconForm
from django.contrib.auth.decorators import login_required
from .uploads import handle_uploaded_file_WITHNAME

@login_required
def Groups(request):
	conf=json.loads(open("static/config/Groups.json","r").read())
	groups=[]
	for i in conf:
		groups.append(Groupe(i,conf[i]['icon']))
	return render(request, "Settings/Settings.html", 
	{
		'config':groups
	})

@login_required
def EditGroup(request,group=None):
	if group:
		conf=json.loads(open("static/config/Groups.json","r").read())

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
	print(request.POST)
	conf=json.loads(open("static/config/Groups.json","r").read())
	dic={
		"formats":json.loads(request.POST['formatlists']),
		"type":request.POST['type']
	}
	icon=None
	if not 'Icon' in request.POST:
		form = UploadIconForm(request.POST, request.FILES)
		if form.is_valid():
			filename=request.POST['groupname']+"."+request.FILES['Icon'].name.split('.')[-1]
			handle_uploaded_file_WITHNAME(request.FILES['Icon'],"static/images/Groups/"+filename,request)
			icon="images/Groups/"+filename

	if request.POST['firstname'] in conf:
		if not icon: icon=conf[request.POST['firstname']]['icon']
		if (request.POST['groupname']!=request.POST['firstname']):
			conf.pop(request.POST['firstname'])
	else:
		if not icon : icon="images/Groups/file.png"

	dic['icon']=icon
	conf[request.POST['groupname']]=dic
	open("static/config/Groups.json","w").write(json.dumps(conf))
	return redirect('../groups')