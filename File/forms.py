from django import forms

class UploadFileForm(forms.Form):
    File = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,'onchange':"getFileName()"}))