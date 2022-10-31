from django.contrib.auth.models import AbstractUser
from django.db import models

roles = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
    ('superuser', 'superuser'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        choices=roles,
        default='user',
        max_length=10,
    )
