#подключаем модули
from django.shortcuts import render,redirect
import json
from .movment import Groupe
from ..forms import UploadIconForm
from django.contrib.auth.decorators import login_required
from .uploads import handle_uploaded_file_WITHNAME
import os
import shutil
#функция отвечает за вывод групп пользователю
@login_required
def Groups(request):
	#проверка на наличие прав суперюзера
	if request.user.is_superuser:
		#получаем конфигурацию групп 
		conf=json.loads(open("static/File/config/Groups.json","r").read())
		groups=[]
		#перебираем конфигурацию и отправляем её пользователю
		for i in conf:
			groups.append(Groupe(i,conf[i]['icon']))
		return render(request, "Settings/Settings.html", 
		{
			'config':groups
		})
	#иначе возвращаем пользователя на главную страницу
	else:   
	    return redirect('../..')
#функция отвечает за удаление групп
@login_required
def DeleteGroup(request,group):
	#проверка на наличие прав суперюзера
	if request.user.is_superuser:
		#получаем конфигурацию групп 
		conf=json.loads(open("static/File/config/Groups.json","r").read())
		#удаляем иконку из статических файлов
		os.remove("static/"+conf[group]['icon'])
		#удаляем группу из списка
		conf.pop(group)
		#записываем изменения
		open("static/File/config/Groups.json","w").write(json.dumps(conf))
		#возвращаемся к списку группп
		return redirect('../groups')
	#иначе возвращаем пользователя на главную страницу
	else:   
	    return redirect('../..')
	
@login_required
def EditGroup(request,group=None):
	#проверка на наличие прав суперюзера
	if request.user.is_superuser:
		if group:
			#получаем конфигурацию групп 
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
	#иначе возвращаем пользователя на главную страницу
	else:   
	    return redirect('../..')


@login_required
def Save(request):
	#проверка на наличие прав суперюзера
	if request.user.is_superuser:
		#получаем конфигурацию групп 
		conf=json.loads(open("static/File/config/Groups.json","r").read())
		#получаем отправленные настройк
		dic={
			"formats":json.loads(request.POST['formatlists']),
			"type":request.POST['type']
		}
		icon=None
		#смотрим отправил ли пользователь иконку
		if not 'Icon' in request.POST:
			#сли да то загружаем иконку в группу
			form = UploadIconForm(request.POST, request.FILES)
			if form.is_valid():
				filename=request.POST['groupname']+"."+request.FILES['Icon'].name.split('.')[-1]
				handle_uploaded_file_WITHNAME(request.FILES['Icon'],"static/File/images/Groups/"+filename,request)
				icon="File/images/Groups/"+filename
		#проверяем на наличие группы
		if request.POST['firstname'] in conf:
			if not icon: icon=conf[request.POST['firstname']]['icon']
			#проверяем на перезапись группы
			if (request.POST['groupname']!=request.POST['firstname']):
				conf.pop(request.POST['firstname'])
		#инче задаём значение по умолчанию если нет иконки
		else:
			if not icon :
				shutil.copyfile("static/File/images/Groups/file.png","static/File/images/Groups/"+request.POST['groupname']+".png")
				icon="File/images/Groups/"+request.POST['groupname']+".png"
		#заносим иконку
		dic['icon']=icon
		#заносим изменения в конфигурацию
		conf[request.POST['groupname']]=dic
		#записываем изменения
		open("static/File/config/Groups.json","w").write(json.dumps(conf))
		#возвращаемся к списку группп
		return redirect('../groups')
	#иначе возвращаем пользователя на главную страницу
	else:   
	    return redirect('../..')
	