#подключаем модули
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
#Данная функция отвечает за асинхронную загрузку файла на сервер
def handle_uploaded_file(f,path,request):
    #создаём файл
    with open(path+'/'+str(f), 'wb+') as destination:
        #перебираем чанки и записываем
        for chunk in f.chunks():
            destination.write(chunk)
        #возвращаемся обратно на страницу откуда происходила закачка
        return redirect(request.scheme + "://" +request.get_host()+"/file/explorer"+path)

#Данная функция также отвечает за загрузку файла на сервер, но в отличие от предыдушей она создаёт файл с именем указанным в пути, а не с тем который присвоен файлу
def handle_uploaded_file_WITHNAME(f,path,request):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        return redirect(request.scheme + "://" +request.get_host()+"/file/explorer"+path)