from django import forms
from .models import MyMessage
from django.forms import Textarea


class MakeMessageForm(forms.ModelForm):
    class Meta:
        text = forms.CharField(label='Escribe Tu Pregunta', required=True)

        model = MyMessage
        fields = ('text',)

        widgets = {
            'text': Textarea(attrs={'class':'form-control'}),
        }