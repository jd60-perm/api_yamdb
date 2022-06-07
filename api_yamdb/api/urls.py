from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CommentViewSet, ReviewViewSet, TitleViewSet, GenreViewSet, CategoryViewSet
)

app_name = 'api'

router = DefaultRouter()

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
    path('', include(router.urls)),
]
