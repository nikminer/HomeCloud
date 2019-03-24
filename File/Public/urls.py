from django.urls import path
from File.Public import actions

urlpatterns = [
    path('', actions.explorePublic),
    path('sharing<path:path>', actions.Shering),
    path('existpseudo',actions.exist),
    path('share/addfile',actions.AddFile),
    path('<str:name>',actions.download)
]