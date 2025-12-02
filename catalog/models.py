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

class AdvancedUser(AbstractUser):
    fio = models.CharField(
        max_length=300,
        verbose_name="ФИО пользователя",
    )

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        pass

class Request(models.Model):
    author = models.ForeignKey(
        AdvancedUser,
        on_delete=models.CASCADE,
        verbose_name="Автор заявки"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Имя заявки"
    )
    description = models.TextField(
        max_length=1000,
        verbose_name="Описание заявки"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Категория заявки"
    )
    photo = models.ImageField(
        upload_to="images/",
        verbose_name="Фото помещения или его план"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания заявки",
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата изменения заявки",
    )

    STATUS_CHOICES = (
        ('n', 'Новая'),
        ('o', 'Принято в работу'),
        ('d', 'Выполнено')
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='n',
        verbose_name="Статус заявки",
    )

    def display_status(self):
        return

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'