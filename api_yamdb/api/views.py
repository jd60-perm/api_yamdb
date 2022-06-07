import secrets
import string
from smtplib import SMTPException

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User
from .serializers import UserSerializer
from api_yamdb.settings import YAMBD_EMAIL

LENGTH_OF_CONF_CODE = 20


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
    data = {
        'email': email,
        'username': username
    }
    serializer = UserSerializer(data=data)
    serializer.is_valid()
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
