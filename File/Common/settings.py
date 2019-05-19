from django.shortcuts import render
import json
from .movment import Groupe

def Groups(request):
	conf=json.loads(open("static/config/Groups.json","r").read())
	groups=[]
	for i in conf:
		groups.append(Groupe(i,conf[i]['icon']))
	return render(request, "Settings/Settings.html", 
	{
		'config':groups
	})

def EditGroup(request,group):
	conf=json.loads(open("static/config/Groups.json","r").read())
	groups=[]
	for i in conf:
		groups.append(Groupe(i,conf[i]['icon']))
	return render(request, "Settings/Settings.html", 
	{
		'config':groups
	})