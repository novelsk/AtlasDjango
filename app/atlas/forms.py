from django.utils import timezone

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, Select, SplitDateTimeWidget, HiddenInput, CheckboxInput,\
    TimeInput
from .models import AtlasUser, SensorMLSettings, ObjectEvent, Object


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Логин', 'class': 'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-control'}))


class UserForm(forms.ModelForm):
    organization = forms.CharField(widget=TextInput, disabled=True, required=False, label='Организация')
    notifications = forms.BooleanField(widget=CheckboxInput(attrs={'class': 'form-check-input'}),
                                       label='Присылать уведомления')

    class Meta:
        model = AtlasUser
        fields = ('last_name', 'first_name', 'middle_name', 'organization', 'division', 'post', 'email',
                  'notifications')


class MLForm(forms.ModelForm):
    error_css_class = 'is-invalid'

    class Meta:
        model = SensorMLSettings
        fields = ('info', 'setting_type', 'setting_ll', 'setting_l', 'setting_h', 'setting_hh', 'point', 'tm_prd',
                  'setting_param_1', 'setting_param_2', 'setting_param_3', 'setting_param_4')


class ObjectEventForm(forms.ModelForm):
    id_object = forms.ModelChoiceField(queryset=Object.objects.all(), widget=HiddenInput)
    status = forms.ChoiceField(choices=ObjectEvent.Statuses.choices, widget=Select(attrs={'class': 'form-control'}),
                               label='Статус')
    date_of_service_planned = forms.SplitDateTimeField(widget=SplitDateTimeWidget(
        attrs={'class': 'form-control choices'}), required=True, initial=timezone.now(), label='Запланировано')
    plan = forms.CharField(min_length=5, max_length=300, widget=TextInput(attrs={'class': 'form-control'}),
                           required=True, label='План работ')
    operating_time = forms.DurationField(widget=TimeInput(attrs={'class': 'form-control'}), required=False,
                                         initial=timezone.timedelta(hours=1), label='Наработка, час')
    date_of_service_completed = forms.SplitDateTimeField(widget=SplitDateTimeWidget(
        attrs={'class': 'form-control choices'}), required=False, label='Выполненно')

    error_css_class = 'is-invalid'

    class Meta:
        model = ObjectEvent
        fields = '__all__'


class ObjectEventFormEdit(ObjectEventForm):
    comment = forms.CharField(min_length=5, max_length=300, widget=TextInput(attrs={'class': 'form-control'}),
                              required=True, label='Комментарий')
