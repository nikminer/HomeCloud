from django.contrib import admin
from django.urls import path
#from file import views
from HomeCloud import views


urlpatterns = [
    #homecloud
    path('',views.index),
    path('cpuusage',views.getCPUpercent),
    path('admin/', admin.site.urls),


    
    #hell
]
