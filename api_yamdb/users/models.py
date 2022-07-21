from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as gtl


CHOICES = [
        ('USER', 'пользователь'),
        ('MODERATOR', 'модератор'),
        ('ADMIN', 'Администратор'),
]


class User(AbstractUser):
    """Для User доступны методы GET, POST, PATCH, DELETE."""

    REQUIRED_FIELDS = ['email']

    first_name = models.CharField(
        gtl('first_name'),
        max_length=150,
    )
    last_name = models.CharField(
        gtl('last_name'),
        max_length=150,
        blank=True,
    )
    email = models.EmailField(
        gtl('email_address'),
        max_length=254,
        unique=True,
    )
    password = models.CharField(
        'Пароль',
        max_length=128,
        blank=False,
        null=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        'Роль',
        max_length=42,
        choices=CHOICES,
        default=CHOICES[0][0],
    )
    confirmation_code = models.CharField(max_length=16, blank=True)

    class Meta:
        ordering = ('username', )
