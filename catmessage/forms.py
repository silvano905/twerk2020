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
    one = forms.CharField(widget=forms.Select(choices=CHOICES), label='Necaxa vs Santos', required=True)
    two = forms.CharField(widget=forms.Select(choices=CHOICES), label='FC Juárez vs León', required=True)
    three = forms.CharField(widget=forms.Select(choices=CHOICES), label='Atlas vs Querétaro', required=True)
    four = forms.CharField(widget=forms.Select(choices=CHOICES), label='Tigres vs Pumas', required=True)
    five = forms.CharField(widget=forms.Select(choices=CHOICES), label='América vs Monterrey', required=True)
    six = forms.CharField(widget=forms.Select(choices=CHOICES), label='Toluca vs Chivas', required=True)
    seven = forms.CharField(widget=forms.Select(choices=CHOICES), label='San Luis vs Cruz Azul', required=True)
    eight = forms.CharField(widget=forms.Select(choices=CHOICES), label='Tijuana vs Puebla', required=True)
    nine = forms.CharField(widget=forms.Select(choices=CHOICES), label='Pachuca vs Mazatlán', required=True)


    class Meta:
        model = Juego
        # exclude = ()
        fields = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

BookModelFormset = modelformset_factory(Juego, form=BookFormset, max_num=25, validate_max=True)