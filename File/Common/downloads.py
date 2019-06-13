#подключаем модуль для взаимодействия с БД
import os
import zipfile
from django.http import StreamingHttpResponse, FileResponse
from .directory import isAccess
from django.contrib.auth.decorators import login_required
import json
#функция отвечает за скачивание файла с сервера
@login_required
def downloadFile(request, path):
	#подготавливаем файловый ответ сервера, т.е. открываем файл читаем побайтовго и через создаём объект класса FileResponse
    response = FileResponse(open(path, 'rb'))
	#задаём потоковый тип скачивания, чтобы пользователь не ждал пока скачается файл, а лишь начал ассинхронную работу
    response['Content-Type'] = 'application/octet-stream'
	#задаём имя файла
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(os.path.split(path)[1])
	#возвращаем ответ сервера
    return response
#функция отвечает за скачивание директории с сервера
@login_required
def downloadFolder(request,path):
	#разбиваем путь на две части (путь к директории и название директории)
	pathes=os.path.split(path)
	#создаём архив 
	zipf = zipfile.ZipFile(path+"/"+pathes[1]+".zip", 'w', zipfile.ZIP_DEFLATED)
	#перебираем директорию для скачивания и все директории в директории и в директориях... пока не переберём вообще всё что содержится в директории
	for root, dirs, files in os.walk(path):
		for file in files:
			if(file != pathes[1]+".zip"):
				#получаем необходимую информацию о файле для добавления в архив
				absfn=os.path.join(root, file)
				zfn = absfn[len(path)+len(os.sep):]
				try:
					#записываем файл в архив
					zipf.write(absfn,zfn)
				except PermissionError:
					#если возникает ощибка с доступом, то пропускаем файл
					pass
	#закрываем архив после записи
	zipf.close()
	#получаем его имя
	fname=pathes[1]+".zip"
	#выызываем функцию отпраки файла пользователю
	return SendFile(path+"/"+fname,fname)
#функция отвечает за скачивание директории и файла с сервера
@login_required
def download(self,path,listf):
	#разбиваем путь на две части (путь к директории и название директории)
	pathes=os.path.split(path)
	#получаем список путей для скачивания из формата JSON
	Files=json.loads(listf)
	if Files:
		#создаём архив 
		zipf = zipfile.ZipFile(path+"/"+pathes[1]+".zip", 'w', zipfile.ZIP_DEFLATED)
		for i in Files:
			#проверяем директория ли этот путь, если да то выполняем действия из def downloadFolder
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
			#иначе выполняем действия из def downloadFile
			else:
				absfn=os.path.join(path,i)
				zipf.write(absfn,i)
		#закрываем архив после записи
		zipf.close()
		#получаем его имя
		fname=pathes[1]+".zip"
		#выызываем функцию отпраки файла пользователю
		return SendFile(path+"/"+fname,fname)
#функцию отвечающая за отпраку файла пользователю
def SendFile(path,fname):
	#функция в функции отвечает за разбиивте файла на чанки и отправку сего пользователю
	def dir_iterator(file_name, chunk_size=512):
		#сначало мы открываем файл в режиме чтения
		with open(file_name,'rb') as f:
			while True:
				#затем в бесконечном цикле читаем 512 байт по умолчанию
				chunk = f.read(chunk_size)
				#и проверяем смогли ли мы прочитать файл или он закончился
				if chunk:
					#если смогли то асинхронно отправляем чанк
					yield chunk
				#иначе закрываем файл и прекращаем бесконечный цикл
				else:
					f.close()
					os.remove(file_name)
					break
	#подготавливаем потоковый запрос с вызовом функции разбиения файлы на чанки
	response = StreamingHttpResponse(dir_iterator(path))
	response['Content-Type'] = 'application/octet-stream'
	#кортедж симоволов для траницлитерации файла
	symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
	#транцилитерация файла
	tr = {ord(a):ord(b) for a, b in zip(*symbols)}
	fname=fname.translate(tr)
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fname)
	#возвращаем запрос
	return response