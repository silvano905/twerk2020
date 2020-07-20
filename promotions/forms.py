from django import forms
from .models import GamesModel
from django.forms import formset_factory
from django.forms import modelformset_factory


class MakeGamesForm(forms.ModelForm):

    games = forms.CharField(label='enter games', required=True)

    class Meta:
        model = GamesModel
        fields = ['games']
