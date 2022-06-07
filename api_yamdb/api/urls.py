from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.send_confirmation_code),
    path('v1/auth/token/', views.get_jwt_token),
]

