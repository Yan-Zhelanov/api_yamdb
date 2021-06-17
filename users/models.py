from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
)


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='E-Mail',
        null=True,
        unique=True,
    )
    bio = models.TextField(
        verbose_name="О себе",
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='Уровень пользователя',
        choices=ROLES,
        default='user',
        max_length=9
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        blank=True,
        null=True,
        max_length=16,
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.username
