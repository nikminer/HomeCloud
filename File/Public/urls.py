from django.urls import path
from File.Public import actions

urlpatterns = [
    path('', actions.explorePublic,name='serverpublic'),
    path('sharing<path:path>', actions.Shering),
    path('existpseudo',actions.exist),
    path('share/addfile',actions.AddFile),
    path('share/getFiles',actions.GetUserFile,name='userpublic'),
    path('share/SwitchVisFile',actions.SwithVisFile,name='SwthVisFile'),
    path('share/delfile',actions.DelPubFile,name='delpubfile'),
    path('<str:name>',actions.download,name='downloadPub')
]