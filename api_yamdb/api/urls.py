from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import UserViewSet
from api.views import (
     CommentViewSet, ReviewViewSet
)


app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.send_confirmation_code),
    path('v1/auth/token/', views.get_jwt_token),
]
