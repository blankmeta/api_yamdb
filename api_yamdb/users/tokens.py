import secrets
from typing import Dict

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(
            timestamp) + six.text_type(user.is_active))


account_activation_token = AccountActivationTokenGenerator()

users_confirmation_codes: Dict = {}


def create_confirmation_code(username: str) -> str:
    """Генерируем и сохраняем код подтверждения."""
    code = secrets.token_hex(nbytes=16)
    users_confirmation_codes[username] = code
    return code


def check_confirmation_code(username: str, confirmation_code: str) -> bool:
    """Проверка кода."""
    if username in users_confirmation_codes.items():
        return users_confirmation_codes[username] == confirmation_code
    return False


def get_tokens_for_user(user: User) -> Dict:
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
