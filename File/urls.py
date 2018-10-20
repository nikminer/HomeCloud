from django.urls import path, re_path
from . import views

urlpatterns = [
    path('back<path:path>',views.back),
    path('explorer<path:path>', views.explorer),
    path('view<path:path>', views.view1),
    path('deldir<path:path>',views.deletedir)
]