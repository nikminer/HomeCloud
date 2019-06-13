#Подключаем модули необходимые для работы программы
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from HomeCloud import views
import django.views.i18n
#Cписок паттернов для парсинга GET запроса браузера
urlpatterns = [
    #DaSH
    #парсинг запросов вне категории
    path('',views.index,name="DaSH-Index"),
    path('i18n/',  include('django.conf.urls.i18n')),
    path('cpuusage',views.getCPUpercent),
    path('swapusage',views.getSwapmemory),
    path('virtualusage',views.getVirtualmemory),
    #DaSH Auth
    #парсинг запросов связанных с аутентификацией пользователя
    path('accounts/login/',views.getlogin),
    path('auth/',views.login),
    path('logout/',views.logout),
    #DaSH Admin
    #парсинг запросов связанных с адменистрированием пользователей
    path('admin/',views.admin),
    path('admin/Users/',views.Users, name="DaSH-USER-LIST"),
    path('admin/Users/create',views.CreateUser),
    path('admin/Users/save',views.Save),
    path('admin/Users/del<str:user>',views.DeleteUser),
    path('admin/Users/chngepass',views.CHPass, name="DaSH-USER-CHANGEPASS"),
    path('admin/Users/setpass/<str:user>',views.SetPass, name="DaSH-USER-SETPASSWORD"),
    #File
    #парсинг запросов и перенаправление запросов свзанных с файловой системой
    re_path(r'^file/',include('File.urls'))
]
