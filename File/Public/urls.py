from django.urls import path
from .actions import Shering,explorePublic,exist,AddFile,download

urlpatterns = [
    path('',explorePublic),
    path('shering<path:path>', Shering),
    path('existpseudo',exist),
    path('shere',AddFile),
    path('<str:name>',download)
]