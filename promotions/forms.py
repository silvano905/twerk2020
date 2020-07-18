from django import forms
from .models import GamesModel


class MakeGamesForm(forms.ModelForm):

    games = forms.CharField(label='enter games', required=True)

    class Meta:
        model = GamesModel
        fields = ['games']