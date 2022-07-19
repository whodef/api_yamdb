from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as gtl


CHOICES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class User(AbstractUser):
    """Для User доступны методы GET, POST, PATCH, DELETE."""

    REQUIRED_FIELDS = ['email']

    name = models.CharField(
        gtl('name'), max_length=150, blank=True,
    )
    email = models.EmailField(
        gtl('email address'), max_length=254, blank=True, unique=True,
    )
    bio = models.TextField(
        'Биография', blank=True,
    )
    role = models.CharField(
        'Роль', max_length=42, choices=CHOICES, default=CHOICES[0][0],
    )
    confirmation_code = models.CharField(max_length=16, blank=True)

    class Meta:
        ordering = ('username', )
