from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')
        help_texts = {
            'username': '',
            'password1': 'Пароль',              # не работает почему-то     | в документации
            'password2': 'Подтвердите пароль',  # и это                     | такого нет
        }
        labels = {
            'username': 'Номер водительского удостоверения',
            'password1': 'Пароль',
            'password2': 'Подтвердите пароль',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=9, label='Номер водительского удостоверения')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

# CONTROL PAGES FORMS BELOW:

class FixateAccidentForm(forms.Form):
    type = forms.ModelChoiceField(queryset=models.Accident.objects.values_list('type', flat=True), empty_label=None, label='Тип', required=False)
    street = forms.CharField(max_length=100, required=False)
    house = forms.CharField(max_length=4, required=False)
    datetime = forms.DateTimeField(required=False)
    culprit = forms.ModelChoiceField(
        # queryset=models.User.objects.order_by('last_name').values_list('last_name', 'first_name'),
        queryset=models.User.objects.all(),
        to_field_name="last_name",
        label='Виновник',
        empty_label=None,
        required=False
        )
    # victim = forms.ModelMultipleChoiceField(
    #     queryset=models.User.objects.order_by('last_name').values_list('last_name', 'first_name'),
    #     label='Пострадавшие',
    #     )

class AddViolationForm(forms.Form):
    add_vio_type = forms.CharField(max_length=255, label='Тип', required=False)
    add_vio_fine = forms.CharField(max_length=6, label='Штраф', required=False)

class SendEmailForm(forms.Form):
    email = forms.CharField(label='Электронный адрес')
    subject = forms.CharField(label='Тема')
    data = forms.CharField(widget=forms.Textarea, label='Сообщение')
