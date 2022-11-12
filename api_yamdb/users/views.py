from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .permissions import (IsAdminOrSuperUserList, IsAdminOrSuperUser)
from .serializers import (SignUpSerializer, GetTokenSerializer, UserSerializer,
                          UserPatchSerializer)
from .tokens import get_tokens_for_user, account_activation_token


class UserList(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminOrSuperUserList,)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

    def update(self, request, *args, **kwargs):
        # Переопределяем сериализатор, если роль - юзер
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        if self.request.user.role == 'user':
            serializer = UserPatchSerializer(instance, data=self.request.data,
                                             partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_object(self):
        username = self.kwargs.get('username')
        if username == 'me':
            if self.request.method == 'DELETE':  # пермишшны возвращают 403,
                raise MethodNotAllowed('DELETE')  # пришлось делать костыль

            return self.request.user

        user_by_username = get_object_or_404(User, username=username)
        self.check_object_permissions(self.request, user_by_username)
        return user_by_username


@api_view(['POST'])
def send_code_view(request):
    serializer = SignUpSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
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
            {'email': email,
             'username': username})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token_view(request):
    serializer = GetTokenSerializer(data=request.data)

    if serializer.is_valid():
        current_user = get_object_or_404(
            User, username=request.data.get('username'))
        return Response(get_tokens_for_user(current_user))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
