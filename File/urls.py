from django.urls import path, re_path
from django.conf.urls import include
from . import views
from .Common.movment import back, explorer,upload_file
from .Common.actions import deletedir, createdir, movedir, deletefile
from .Common.downloads import downloadFile,downloadFolder
from .Common.Preview import ViewSwitcher
from .Common.directory import isExist


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
    #downloading
    path('downloadfile<path:path>', downloadFile),
    path('downloadfolder<path:path>', downloadFolder),
    #Preview
    path('view<path:path>', ViewSwitcher),
    #lite
    re_path(r'^lite/',include('File.Lite.urls'))
]