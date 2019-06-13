#подключаем модуль для взаимодействия с БД
from django.db import models

#Создаём модель публичного файла для последующей миграции
class Publicfile(models.Model):
    pseudoname=models.CharField(max_length=255,unique=True,primary_key=True)
    Sharinguser=models.CharField(max_length=255,default='')
    path=models.FilePathField(max_length=100000)
    isvisible=models.CharField(max_length=5,default="True")
    isdownloaded=models.CharField(max_length=3,default="on")