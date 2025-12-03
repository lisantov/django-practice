from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

from .models import AdvancedUser, Request


class RegistrationForm(UserCreationForm):
    agreement = forms.BooleanField(
        required=True,
        label='Я согласен на обработку персональных данных'
    )

    def clean_fio(self):
        cleaned_fio = self.cleaned_data['fio']
        regex = re.compile(r'[А-ЯЁ][А-яЁё\s\-]+')
        if not re.fullmatch(regex, cleaned_fio):
            raise ValidationError(_('ФИО может содержать только кириллицу, дефисы и пробелы'))
        return cleaned_fio

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 3:
            raise ValidationError(_('В пароле должно быть не меньше трёх символов'))
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            self.cleaned_data['password2'] = ''
            raise ValidationError(_('Пароли не совпадают'))

        return password2

    class Meta:
        model = AdvancedUser
        fields = ('fio', 'username', 'email', 'password1', 'password2')

class RequestForm(forms.ModelForm):
    def clean_photo(self):
        photo = self.cleaned_data['photo']
        valid_formats = ['png', 'jpg', 'jpeg', 'bmp']
        valid_size = 2

        if not photo:
            raise ValidationError(_('Поле не может быть пустым'))
        elif not photo.name.split('.')[-1] in valid_formats:
            raise ValidationError(_(f'Принимаются только файлы формата: {', '.join(valid_formats)}'))
        elif not photo.size / 1024 / 1024 <= valid_size:
            raise ValidationError(_(f'Файл должен весить не более {valid_size}Мб'))
        return photo

    class Meta:
        model = Request
        fields = ('title', 'description', 'category', 'photo')

class ChangeStatusForm(forms.ModelForm):
    def clean_photo_after(self):
        if self.cleaned_data['status'] == 'd':
            photo = self.cleaned_data['photo_after']
            valid_formats = ['png', 'jpg', 'jpeg', 'bmp']
            valid_size = 2

            if not photo:
                raise ValidationError(_('Поле не может быть пустым'))
            elif not photo.name.split('.')[-1] in valid_formats:
                raise ValidationError(_(f'Принимаются только файлы формата: {', '.join(valid_formats)}'))
            elif not photo.size / 1024 / 1024 <= valid_size:
                raise ValidationError(_(f'Файл должен весить не более {valid_size}Мб'))
            return photo
        return ''

    def clean_commentary(self):
        if self.cleaned_data['status'] == 'o':
            data = self.cleaned_data['commentary']
            if data:
                raise ValidationError(_('Поле не может быть пустым'))
            return data
        return ''

    class Meta:
        model = Request
        fields = ('status', 'commentary', 'photo_after')