from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    db = forms.FileField()
    
    
class RegistrationDbForm(forms.Form):
    uid = forms.CharField(max_length=25)
    