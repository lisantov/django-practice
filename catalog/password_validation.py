from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class PasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 3:
            raise ValidationError(_('ФИО может содержать только кириллицу, дефисы и пробелы'))

    def get_help_text(self):
        return _('Введите пароль')