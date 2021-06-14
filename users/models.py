from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('U', 'user'),
    ('M', 'moderator'),
    ('A', 'admin')
)

class CustomUser(AbstractUser):
    bio = models.TextField(
        verbose_name="О себе",
        blank=True,
        null=True,
    )
    role = models.IntegerField(
        verbose_name='Уровень пользователя',
        choices=ROLES,
        default='U',
    )
    code_confirmation = models.CharField(
        verbose_name='Код подтверждения',
        blank=True,
        null=True,
        max_length=16,
    )