from django.urls import path, include
from rest_framework import routers

from .views import ReviewViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                   basename=r'titles/(?P<title_id>\d+)/reviews')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]