from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import AtlasUser, SensorMLSettings


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Login'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))


class UserForm(forms.ModelForm):
    organization = forms.CharField(widget=TextInput, disabled=True, required=False, label='Организация')

    class Meta:
        model = AtlasUser
        fields = ('last_name', 'first_name', 'middle_name', 'organization', 'division', 'post', 'email')


class MLForm(forms.ModelForm):
    error_css_class = 'is-invalid'

    class Meta:
        model = SensorMLSettings
        fields = ('info', 'setting_type', 'setting_ll', 'setting_l', 'setting_h', 'setting_hh', 'point', 'tm_prd',
                  'setting_param_1', 'setting_param_2', 'setting_param_3', 'setting_param_4')
