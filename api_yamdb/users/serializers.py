from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User, ROLES
from users.tokens import account_activation_token


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(required=False)
    role = serializers.ChoiceField(choices=ROLES, default='user',
                                   required=False)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Пользователь не может иметь такое имя')

        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                'Пользователь с такой почтой уже существует')

        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует')
        return data


class UserPatchSerializer(UserSerializer):
    role = serializers.ChoiceField(choices=ROLES, default='user',
                                   required=False, read_only=True)


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()

    validate = UserSerializer.validate


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        current_user = get_object_or_404(User, username=data['username'])
        if not account_activation_token.check_token(current_user,
                                                    data['confirmation_code']):
            raise serializers.ValidationError('Неверный код подтверждения')
        return data
