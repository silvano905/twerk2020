from django import forms
from .models import MakeTip
from django.forms import Textarea, TextInput, ImageField


class MakePostForm(forms.ModelForm):
    creativity = forms.IntegerField(required=False)
    sexy = forms.IntegerField(required=False)
    quality = forms.IntegerField(required=False)
    outfit = forms.IntegerField(required=False)
    post_pict_link = forms.Textarea(attrs={'placeholder': 'Please enter the  description'})
    post_pic = forms.URLField(required=False)

    class Meta:
        model = MakeTip
        fields = ['post_pic', 'title', 'creativity', 'sexy', 'quality', 'outfit', 'post_pict_link']
        labels = {
            'post_pic': 'Selecciona video'
        }

        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'post_pict_link': TextInput(attrs={'class': 'form-control'}),
        }
