from django.db import models
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Имя категории",
        verbose_name="Имя категории"
    )

    def __str__(self):
        return self.name

class Request(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Имя заявки",
        verbose_name="Имя заявки"
    )
    description = models.TextField(
        max_length=1000,
        help_text="Описание заявки",
        verbose_name="Описание заявки"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        help_text="Категория заявки",
        verbose_name="Категория заявки"
    )
    photo = models.ImageField(
        upload_to="images/",
        help_text="Фотография заявки",
        verbose_name="Фотография заявки"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания заявки",
        help_text="Дата создания заявки"
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата изменения заявки",
        help_text="Дата изменения заявки"
    )

    CATEGORY_CHOICES = (
        ('n', 'Новая'),
        ('o', 'Принято в работу'),
        ('d', 'Выполнено')
    )

    status = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
        default='n',
        verbose_name="Статус заявки",
        help_text="Статус заявки"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class AdvancedUser(AbstractUser):
    fio = models.CharField(
        max_length=300,
        verbose_name="ФИО пользователя",
        help_text="ФИО"
    )

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        pass