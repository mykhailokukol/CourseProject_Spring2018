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

class AddViolationForm(forms.Form):
    type = forms.CharField(max_length=255, label='Тип')
    fine = forms.CharField(max_length=6, label='Штраф')

class ChangeViolationForm(forms.Form):
    violation = forms.ModelChoiceField(queryset=models.Violation.objects.values_list('type', flat=True), empty_label=None, label='Выберите нарушение')
    type = forms.CharField(max_length=255, label='Тип')
    fine = forms.CharField(max_length=6, label='Штраф')

class DeleteViolationForm(forms.Form):
    violation = forms.ModelChoiceField(queryset=models.Violation.objects.values_list('type', flat=True), empty_label=None, label='Выберите нарушение')

class AddAccidentForm(forms.Form):
    type = forms.CharField(max_length=255, label='Тип')

class ChangeAccidentForm(forms.Form):
    accident = forms.ModelChoiceField(queryset=models.Accident.objects.values_list('type', flat=True), empty_label=None, label='Выберите тип ДТП')
    type = forms.CharField(max_length=255, label='Заменить на')

class DeleteAccidentForm(forms.Form):
    accident = forms.ModelChoiceField(queryset=models.Accident.objects.values_list('type', flat=True), empty_label=None, label='Выберите тип ДТП')

class SendEmailForm(forms.Form):
    email = forms.CharField(label='Электронный адрес')
    subject = forms.CharField(label='Тема')
    data = forms.CharField(widget=forms.Textarea, label='Сообщение')

class FixateAccidentForm(forms.Form):
    street = forms.CharField(max_length=255, label='Улица')
    house = forms.CharField(max_length=4, label='Номер дома')
    datetime = forms.DateTimeField(label='Дата и время')
    type = forms.ModelChoiceField(queryset=models.Accident.objects.all(), empty_label=None, label='Тип ДТП')
    drivers = forms.ModelMultipleChoiceField(queryset=models.Driver.objects.all(), label='Водители')
    pedestrians = forms.ModelMultipleChoiceField(queryset=models.User.objects.all(), label='Пешеходы', required=False)
    na_pedestrians = forms.CharField(max_length=None, required=False, widget=forms.Textarea, label='Незарегестрированные пешеходы')

class FixateViolationForm(forms.Form):
    street = forms.CharField(max_length=255, label='Улица')
    house = forms.CharField(max_length=4, label='Номер дома')
    datetime = forms.DateTimeField(label='Дата и время')
    type = forms.ModelChoiceField(queryset=models.Violation.objects.all(), empty_label=None, label='Тип нарушения')
    car = forms.ModelChoiceField(queryset=models.Car.objects.all(), empty_label=None, label='Автомобиль')

class OwnerInfoForm(forms.Form):
    owner = forms.ModelChoiceField(queryset=models.User.objects.all(), empty_label=None, label='Владелец')










#
