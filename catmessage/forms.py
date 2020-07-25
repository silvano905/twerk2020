from django import forms
from .models import MyMessage, Juego
from django.forms import Textarea
from django.forms import modelformset_factory

class MakeMessageForm(forms.ModelForm):
    class Meta:
        text = forms.CharField(label='Escribe Tu Pregunta', required=True)

        model = MyMessage
        fields = ('text',)

        widgets = {
            'text': Textarea(attrs={'class':'form-control'}),
        }



class BookFormset(forms.ModelForm):

    CHOICES = (
        ('', 'Seleciona tu pronóstico aqui'),
        ('L', 'L'),
        ('E', 'E'),
        ('V', 'V'),
    )
    one = forms.CharField(widget=forms.Select(choices=CHOICES), label='Puebla vs Cruz Azul', required=True)
    two = forms.CharField(widget=forms.Select(choices=CHOICES), label='Juárez vs Necaxa', required=True)
    three = forms.CharField(widget=forms.Select(choices=CHOICES), label='América vs Tijuana', required=True)
    four = forms.CharField(widget=forms.Select(choices=CHOICES), label='Tigres vs Pachuca', required=True)
    five = forms.CharField(widget=forms.Select(choices=CHOICES), label='Atlas vs Pumas', required=True)
    six = forms.CharField(widget=forms.Select(choices=CHOICES), label='Toluca vs San Luis', required=True)
    seven = forms.CharField(widget=forms.Select(choices=CHOICES), label='Querétaro vs Mazatlán', required=True)
    eight = forms.CharField(widget=forms.Select(choices=CHOICES), label='Santos vs Chivas', required=True)
    nine = forms.CharField(widget=forms.Select(choices=CHOICES), label='León vs Monterrey', required=True)


    class Meta:
        model = Juego
        # exclude = ()
        fields = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

BookModelFormset = modelformset_factory(Juego, form=BookFormset, max_num=25, validate_max=True)