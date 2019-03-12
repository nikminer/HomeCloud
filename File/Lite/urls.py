from django.urls import path
from .movment import explorerDir


urlpatterns = [
    path('explorerdir<path:path>', explorerDir)
]