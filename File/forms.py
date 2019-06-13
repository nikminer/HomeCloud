#подключаем модуль для взаимодействия с БД
from django import forms
#форма для загрузки файлов на сервер с предустановленными параметрами
class UploadFileForm(forms.Form):
    File = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,'onchange':"getFileName()"}))
#форма для загрузки иконок группы на сервер
class UploadIconForm(forms.Form):
    Icon = forms.FileField(widget=forms.ClearableFileInput(attrs={'id': 'fileicon','name':"icon"}),label='',required=False)