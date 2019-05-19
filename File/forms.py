from django import forms

class UploadFileForm(forms.Form):
    File = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,'onchange':"getFileName()"}))

class UploadIconForm(forms.Form):
    Icon = forms.FileField(widget=forms.ClearableFileInput(attrs={'id': 'fileicon','name':"icon"}),label='',required=False)