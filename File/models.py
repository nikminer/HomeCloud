from django.db import models

class Publicfile(models.Model):
    pseudoname=models.CharField(max_length=255,unique=True,primary_key=True)
    Sharinguser=models.CharField(max_length=255,default='')
    path=models.FilePathField(max_length=100000)
    isvisible=models.CharField(max_length=5,default="false")
    isdownloaded=models.CharField(max_length=3,default="on")