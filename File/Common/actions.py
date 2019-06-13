#подключаем модуль для взаимодействия с БД
from django.shortcuts import redirect
import shutil,os
import json
from django.contrib.auth.decorators import login_required
#функция для удаление директории
@login_required
def deletedir(request):
	#удаляем директорию вместе со всеми файлами
	shutil.rmtree(request.POST['delpath'])
	#перемещаемя в родительскую директорию
	return redirect(request.scheme + "://" +request.get_host()+"/file/back"+request.POST['delpath'])
#функция для создания директории
@login_required
def createdir(request):
	#получаем путь к новой директории
	path=request.POST['dirpath']+request.POST['path']
	#создаём директорию
	os.mkdir(path)
	#обновляем страницу с директорией
	return redirect(request.scheme + "://" +request.get_host()+"/file/back"+path)
#функция для перемещения директории
@login_required
def movedir(request):
	#перемещаем директорию
    shutil.move(request.POST.get('originalpath'),request.POST.get('destionalpath'))
	#переходим куда переместили директорию
    return redirect(request.scheme + "://" +request.get_host()+"/file/explorer"+request.POST.get('destionalpath')) 
#функция для удаления файла
@login_required
def deletefile(request):
	#удаляем файл
    os.remove(request.POST['delpath'])
	#делаем запрос для обновления директории
    return redirect(request.scheme + "://" +request.get_host()+"/file/back"+request.POST['delpath'])
#функция для множественного удаления файлов
@login_required
def delete(request):
	#получаем список элементов необходимых для удаления в JSON формате
	listF=json.loads(request.POST['list'])
	#получаем путь директории в которой будет происходить удаление
	path=request.POST['delpath']
	#перебираем список удаляемых элементов
	for i in listF:
		#проверяем папка ли элемент если да то удаляем как папку
		if os.path.isdir(path+"/"+i):
			shutil.rmtree(path+"/"+i)
		#иначе удаляем как файл
		else:
			os.remove(path+"/"+i)
	#возвращаемся в проводник с новой структурой
	return redirect(request.scheme + "://" +request.get_host()+"/file/explorer"+path)