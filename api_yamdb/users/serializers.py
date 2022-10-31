from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User
from users.tokens import check_confirmation_code, account_activation_token


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Пользователь не может иметь такое имя')
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует')
        return data


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        current_user = get_object_or_404(User, username=data['username'])
        if not account_activation_token.check_token(current_user,
                                                    data['confirmation_code']):
            raise serializers.ValidationError('Неверный код подтверждения')
        return data
