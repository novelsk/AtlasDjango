from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import AtlasUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Login'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))


class UserForm(forms.ModelForm):
    organization = forms.CharField(widget=TextInput, disabled=True, label='Организация')

    class Meta:
        model = AtlasUser
        fields = ('last_name', 'first_name', 'middle_name', 'organization', 'division', 'post', 'email')
