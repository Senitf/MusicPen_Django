from django import forms
from .models import NoteIMG

class ImageForm(forms.ModelForm):
    class Meta:
        model = NoteIMG
        fields = ('file',)