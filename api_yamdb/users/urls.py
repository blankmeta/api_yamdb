from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import send_code_view, get_token_view, UserDetail, UserList

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/auth/signup/', send_code_view),
    path('v1/auth/token/', get_token_view),
    path('v1/users/<str:username>/', UserDetail.as_view()),
    path('v1/users/', UserList.as_view()),
]
