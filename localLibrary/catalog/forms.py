import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Введите дату от сегодня до 4 недель (по-умолчанию 3)",
        label=_("Новая дата возврата")
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Неверная дата - введённая дата в прошлом'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Неверная дата - введённая дата старше 4-x недель'))

        return data