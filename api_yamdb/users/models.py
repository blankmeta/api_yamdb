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

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        ordering = ['id']
