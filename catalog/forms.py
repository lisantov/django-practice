from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

from .models import AdvancedUser

class RegistrationForm(UserCreationForm):
    agreement = forms.BooleanField(
        required=True,
        label='Я согласен на обработку персональных данных'
    )

    def clean_fio(self):
        cleaned_fio = self.cleaned_data['fio']
        regex = re.compile(r'[А-Яа-яЁё][А-Яа-яЁё\s\-]+')
        if not re.fullmatch(regex, cleaned_fio):
            raise ValidationError(_('ФИО может содержать только кириллицу, дефисы и пробелы'))
        return cleaned_fio

    class Meta:
        model = AdvancedUser
        fields = ('fio', 'username', 'email', 'password1', 'password2')