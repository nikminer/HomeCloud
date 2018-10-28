from django.urls import path, re_path
from . import views
from .Common.movment import back, explorer
from .Common.actions import deletedir,createdir,movedir

urlpatterns = [
    path('back<path:path>',back),
    path('explorer<path:path>', explorer),
    path('view<path:path>', views.view1),
    path('deldir<path:path>', deletedir),
    path('mkdir<path:path>', createdir),
    path('movedir<path:path>+<path:path1>', movedir),
]