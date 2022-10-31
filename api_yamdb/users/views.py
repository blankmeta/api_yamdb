from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializers import SignUpSerializer, GetTokenSerializer
from .tokens import create_confirmation_code, get_tokens_for_user, \
    account_activation_token


@api_view(['POST'])
def send_code_view(request):
    serializer = SignUpSerializer(data=request.data)

    if serializer.is_valid():
        username = request.data.get('username')
        email = request.data.get('email')

        current_user = User.objects.create_user(username=username, email=email)

        send_mail(
            'Подтверждение регистрации',
            account_activation_token.make_token(current_user),
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return Response(
            {'message': f'Код подтверждения для получения токена'
                        f' отправлен на почту '
                        f'{email}'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token_view(request):
    serializer = GetTokenSerializer(data=request.data)

    if serializer.is_valid():
        current_user = get_object_or_404(
            User, username=request.data.get('username'))
        return Response(get_tokens_for_user(current_user))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
