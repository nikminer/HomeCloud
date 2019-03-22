from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
#from file import views
from HomeCloud import views


urlpatterns = [
    #homecloud
    path('',views.index),
    path('cpuusage',views.getCPUpercent),
    path('accounts/login/',views.getlogin),
    path('auth/',views.login),
    path('logout/',views.logout),
    path('admin/', admin.site.urls),
    
    re_path(r'^file/',include('File.urls'))
]
