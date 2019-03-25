from django.urls import path
from .movment import explorerDir,explorerFiles


urlpatterns = [
    path('explorerdir<path:path>', explorerDir),
    path('explorerfiles<path:path>', explorerFiles)
]