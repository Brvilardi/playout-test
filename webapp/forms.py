from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class' : 'form-control',
                                                                        'id' : 'title',
                                                                        'placeholder': 'Title'}))


    file = forms.FileField()