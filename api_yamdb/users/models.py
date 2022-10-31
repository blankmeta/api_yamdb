from django.contrib.auth.models import AbstractUser
from django.db import models

roles = (
    ('US', 'user'),
    ('MD', 'moderator'),
    ('AD', 'admin'),
    ('SP', 'superuser'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        choices=roles,
        default='user',
        max_length=2,
    )
