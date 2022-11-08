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
    is_admin = models.BooleanField(default=False, )
    is_moderator = models.BooleanField(default=False, )

    def change_role_permission(self, new_role):
        role_to_permission_field = {
            'admin': self.is_admin,
            'moderator': self.is_moderator
        }
        for role_permission in role_to_permission_field.values():
            role_permission = False
        if new_role in role_to_permission_field:
            role_to_permission_field[new_role] = True

    def save(self, *args, **kwargs):
        self.change_role_permission(self.role)

    class Meta:
        ordering = ['id']
