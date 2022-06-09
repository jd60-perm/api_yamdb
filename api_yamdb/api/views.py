import secrets
import string
from smtplib import SMTPException

from api.permissions import AdminOrGetMethod, AuthorStaffOrReadOnly, IsAdmin
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleReadSerializer, TitleSerializer,
                             UserSerializer)
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from api_yamdb.settings import LENGTH_OF_CONF_CODE, YAMBD_EMAIL

from .filters import TitleFilter
from .mixins import PostListDelMixin


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorStaffOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorStaffOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


@api_view(['POST'])
def send_confirmation_code(request):
    email = request.data.get('email')
    username = request.data.get('username')
    if (User.objects.filter(username=username).exists()
            or User.objects.filter(email=email).exists()):
        return Response(
            {"result": "Пользователь с такими данными уже существует."},
            status=status.HTTP_400_BAD_REQUEST
        )
    if username == 'me':
        return Response('Нельзя создать пользователя с ником me',
                        status=status.HTTP_400_BAD_REQUEST)
    data = {
        'email': email,
        'username': username
    }
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    letters_and_digits = string.ascii_letters + string.digits
    confirmation_code = ''.join(secrets.choice(
        letters_and_digits) for i in range(LENGTH_OF_CONF_CODE))
    user = User.objects.get(username=username)
    user.confirmation_code = confirmation_code
    user.save()
    try:
        send_mail(
            'YAMDB подтверждение регистрации',
            f'Добрый день! Код подтверждения {confirmation_code}.',
            YAMBD_EMAIL,
            [email],
            fail_silently=False
        )
    except SMTPException:
        return Response('Ошибка при отправке email',
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    username = request.data.get('username')
    if username is None:
        response = {'username': 'Не указано имя пользователя'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=username)
    if user.confirmation_code != request.data.get('confirmation_code'):
        response = {'confirmation_code': 'Некорректный код подтверждения'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    token_refresh = RefreshToken.for_user(user)
    token = str(token_refresh.access_token)
    response = {'token': token}
    return Response(response, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    search_fields = ['username', ]

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['GET', 'PATCH'], url_path='me')
    def get_yourself_info(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                instance=request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrGetMethod,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return TitleSerializer
        return TitleReadSerializer


class GenreViewSet(PostListDelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrGetMethod,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(PostListDelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrGetMethod,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
