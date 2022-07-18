from django.utils import timezone
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, Select, DateTimeInput, HiddenInput, CheckboxInput
from .models import AtlasUser, SensorMLSettings, ObjectEvent, Object


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Логин', 'class': 'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-control'}))


class UserForm(forms.ModelForm):
    organization = forms.CharField(widget=TextInput, disabled=True, required=False, label='Организация')
    notifications = forms.BooleanField(widget=CheckboxInput(attrs={'class': 'form-check-input'}),
                                       required=False, label='Присылать уведомления на почту')

    class Meta:
        model = AtlasUser
        fields = ('last_name', 'first_name', 'middle_name', 'organization', 'division', 'post', 'email',
                  'notifications')


class CreateUserForm(forms.ModelForm):
    error_css_class = 'is-invalid'

    class Meta:
        model = AtlasUser
        fields = ('username', 'password', 'email')


class MLForm(forms.ModelForm):
    error_css_class = 'is-invalid'

    class Meta:
        model = SensorMLSettings
        fields = ('info', 'setting_type', 'setting_ll', 'setting_l', 'setting_h', 'setting_hh', 'point', 'tm_prd',
                  'setting_param_1', 'setting_param_2', 'setting_param_3')
        labels = {
            'setting_ll': 'Нижний аварийный уровень (LL)',
            'setting_l': 'Нижний предупредительный уровень (L)',
            'setting_h': 'Верхний предупредительный уровень (H)',
            'setting_hh': 'Верхний аварийный уровень (HH)',
            'point': 'Размер обучающей выборки, мин',
            'tm_prd': 'Размер рабочей выборки, мин',
            'setting_param_1': 'Погрешность режима ST',
            'setting_param_2': 'Погрешность режима ML',
            'setting_param_3': 'Период выхода из строя, дней'
        }


class ObjectEventForm(forms.ModelForm):
    id_object = forms.ModelChoiceField(queryset=Object.objects.all(), widget=HiddenInput)
    status = forms.ChoiceField(choices=ObjectEvent.Statuses.choices, widget=Select(attrs={'class': 'form-control'}),
                               label='Статус')

    date_of_service_planned = forms.DateTimeField(widget=DateTimeInput(
        attrs={'class': 'form-control choices'}), required=True, initial=timezone.now(), label='Запланировано')

    plan = forms.CharField(min_length=5, max_length=300, widget=TextInput(attrs={'class': 'form-control'}),
                           required=True, label='План работ')

    date_of_service_completed = forms.DateTimeField(widget=DateTimeInput(
        attrs={'class': 'form-control choices'}), required=False, label='Выполненно')

    error_css_class = 'is-invalid'

    class Meta:
        model = ObjectEvent
        fields = '__all__'


class ObjectEventFormEdit(ObjectEventForm):
    comment = forms.CharField(min_length=5, max_length=300, widget=TextInput(attrs={'class': 'form-control'}),
                              required=True, label='Комментарий')


class ObjectEditForm(forms.ModelForm):

    class Meta:
        model = Object
        fields = '__all__'
