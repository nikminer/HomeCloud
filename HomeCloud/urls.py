from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
#from file import views
from HomeCloud import views
import django.views.i18n

urlpatterns = [
    #homecloud
    path('',views.index),
    path('i18n/',  include('django.conf.urls.i18n')),
    path('cpuusage',views.getCPUpercent),
    path('swapusage',views.getSwapmemory),
    path('virtualusage',views.getVirtualmemory),
    path('accounts/login/',views.getlogin),
    path('auth/',views.login),
    path('logout/',views.logout),
    path('admin/', admin.site.urls),
    
    re_path(r'^file/',include('File.urls'))
]
