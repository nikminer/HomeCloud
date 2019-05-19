from django.urls import path, re_path
from django.conf.urls import include
from . import views
from .Common.movment import back, explorer,upload_file
from .Common.actions import deletedir, createdir, movedir, deletefile,delete
from .Common.downloads import downloadFile,downloadFolder,download
from .Common.Preview import ViewSwitcher
from .Common.directory import isExist
from .Common.settings import Groups,EditGroup,Save

urlpatterns = [
    #movment
    path('back<path:path>',back),
    path('explorer<path:path>', explorer),
    path('uploadfile', upload_file,name="upload"),
    #actions
    path('deldir', deletedir),
    path('mkdir', createdir),
    path('exdir', isExist),
    path('movedir', movedir),
    path('delfile',deletefile),
	path('delete',delete),
    #downloading
    path('downloadfile<path:path>', downloadFile),
    path('downloadfolder<path:path>', downloadFolder),
	path('download<path:path>+<str:listf>',download),
	#settings
    path('settings/groups/edit<str:group>',EditGroup),
    path('settings/groups/edit',EditGroup),
	path('settings/groups/',Groups),
    path('settings/groups/save',Save),
    #Preview
    path('view<path:path>', ViewSwitcher),
    #lite
    re_path(r'^lite/',include('File.Lite.urls')),
    #public
    re_path(r'^public/',include('File.Public.urls'))
]