from django.contrib.auth.models import AbstractUser
from django.db import models

from .roles import USER, MODERATOR, ADMIN

ROLES = (
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
)


def get_max_role_length(roles):
    max_length = 0
    for role, _ in roles:
        if len(role) > max_length:
            max_length = len(role)
    return max_length


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='E-Mail',
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
        default=USER,
        max_length=get_max_role_length(ROLES)
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        blank=True,
        null=True,
        max_length=64,
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.username
