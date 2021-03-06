from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea, TextInput


class UserFormRegistration(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "password1", "id": "myInput"}), max_length=40, label="contraseña")
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "inputPassword", 'placeholder': 'Junta tu nombre sin dejar espacio en el medio'}), max_length=40, label="Primer nombre o apodo (ejemplo: luis9)")
    email = forms.CharField(widget=forms.TextInput(attrs={'class': "inputemail"}), max_length=60, label="Dirección de correo electrónico")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']


class UserFormProfile(forms.ModelForm):
    description = forms.CharField(label='Agrega tu numero de telefono', required=True)

    class Meta:
        model = Profile
        fields = ('description',)

        widgets = {
            'description': TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].label = "Descripción"


# -------------------------to update---------------------------------------

class UserFormProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', ]

        # widgets = {
        #     'description': Textarea(attrs={'class': 'form-control'}),
        # }


class UserFormCreationFormUpdate(forms.ModelForm):
    User._meta.get_field('email')._unique = True
    User._meta.get_field('username')._unique = True

    class Meta:
        model = User
        fields = ('username',)

        widgets = {
            'username': TextInput(attrs={'class': 'form-control'})
        }