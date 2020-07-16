from django import forms
from .models import MakeTip
from django.forms import Textarea, TextInput, ImageField
from django.utils.translation import ugettext_lazy as _

class MakePostForm(forms.ModelForm):
    CHOICES = (
        ('', 'seleciona aqui'),
        ('L', 'L'),
        ('E', 'E'),
        ('V', 'V'),
    )
    one = forms.CharField(widget=forms.Select(choices=CHOICES), label='Chivas vs América', required=True)
    two = forms.CharField(widget=forms.Select(choices=CHOICES), label='Monterrey vs Cruz Azul', required=True)
    three = forms.CharField(widget=forms.Select(choices=CHOICES), label='León vs Santos', required=True)
    four = forms.CharField(widget=forms.Select(choices=CHOICES), label='Pumas vs Tigres', required=True)
    five = forms.CharField(widget=forms.Select(choices=CHOICES), label='Juárez vs Morelia', required=True)
    six = forms.CharField(widget=forms.Select(choices=CHOICES), label='Puebla vs Pachuca', required=True)
    seven = forms.CharField(widget=forms.Select(choices=CHOICES), label='Querétaro vs San Luis', required=True)
    eight = forms.CharField(widget=forms.Select(choices=CHOICES), label='Necaxa vs Toluca', required=True)
    nine = forms.CharField(widget=forms.Select(choices=CHOICES), label='Tijuana vs Atlas', required=True)


    class Meta:
        model = MakeTip
        fields = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']




        # widgets = {
        #     'one': TextInput(attrs={'class': 'jj'}),
        # }
