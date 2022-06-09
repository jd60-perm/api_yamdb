from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import UserViewSet

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
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.send_confirmation_code),
    path('v1/auth/token/', views.get_jwt_token),
]
