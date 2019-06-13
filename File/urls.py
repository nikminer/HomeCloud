#Подключаем модули необходимые для работы программы
from django.urls import path, re_path
from django.conf.urls import include
from . import views
from .Common.movment import back, explorer,upload_file
from .Common.actions import deletedir, createdir, movedir, deletefile,delete
from .Common.downloads import downloadFile,downloadFolder,download
from .Common.Preview import ViewSwitcher
from .Common.directory import isExist
from .Common.settings import Groups,EditGroup,Save,DeleteGroup
#Cписок паттернов для парсинга GET запроса браузера
urlpatterns = [
    #movment
    #парсинг запросов отвечающие за перемещения по файловой системе 
    path('back<path:path>',back),
    path('explorer<path:path>', explorer),
    path('uploadfile', upload_file,name="upload"),
    #actions
    #парсинг запросов отвечающие за действия с файловой системе  
    path('deldir', deletedir),
    path('mkdir', createdir),
    path('exdir', isExist),
    path('movedir', movedir),
    path('delfile',deletefile),
	path('delete',delete),
    #downloading
    #парсинг запросов отвечающие за скачивание с файловой системе  
    path('downloadfile<path:path>', downloadFile),
    path('downloadfolder<path:path>', downloadFolder),
	path('download<path:path>+<str:listf>',download),
	#settings
    #парсинг запросов отвечающие за настройку групп  
    path('settings/groups/edit<str:group>',EditGroup),
    path('settings/groups/del<str:group>',DeleteGroup),
    path('settings/groups/edit',EditGroup),
	path('settings/groups/',Groups),
    path('settings/groups/save',Save),
    #Preview
    #парсинг запросов отвечающие за превью файлов  
    path('view<path:path>', ViewSwitcher),
    #lite
    #парсинг запросов и перенаправление запросов свзанных с подсистемой Lite(минималистичный File)
    re_path(r'^lite/',include('File.Lite.urls')),
    #public
    #парсинг запросов и перенаправление запросов свзанных с подсистемой Public
    re_path(r'^public/',include('File.Public.urls'))
]