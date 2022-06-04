from django.core.validators import (
    MaxValueValidator, MinValueValidator
)
from datetime import date
from django.db import models

from django.contrib.auth.models import AbstractUser

USER_ROLES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
]


class User(AbstractUser):
    username = models.CharField(
        'Логин пользователя',
        max_length=200,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        'Адрес почты',
        max_length=200,
        unique=True,
        blank=False,
        null=False,
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=200,
        choices=USER_ROLES,
        default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True, )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
    )

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == USER_ROLES[1][1]

    @property
    def is_moderator(self):
        return self.role == USER_ROLES[2][1]

    @property
    def is_admin(self):
        return self.role == USER_ROLES[3][1]


class Category(models.Model):
    name = models.CharField(
        unique=True,
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )

    class Meta:
        ordering = ('-id',)


class Genre(models.Model):
    name = models.CharField(
        unique=True,
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )

    class Meta:
        ordering = ('-id',)


class Title(models.Model):
    name = models.TextField()
    year = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(
                limit_value=date.today().year,
                message='Title\'s year can not be greater than current year',
            )
        ]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
    )
    genre = models.ManyToManyField(Genre)
    description = models.TextField()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name[:15]


class Review(models.Model):
    MARKS = [(i, str(i)) for i in range(1, 11)]


    title = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название произведения'
    )
    text = models.TextField(
        verbose_name='Текст отзыва')
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва')
    score = models.CharField(
        max_length=1,
        choices=MARKS,
        verbose_name='Оценка произведения',
        validators=(
            MaxValueValidator(
                10, 'Оценка не может быть более 10.'),
            MinValueValidator(
                1, 'Оценка не может быть менее 1.'),
        ),
        blank=False,
        null=False,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва'
    )

    class Meta:
       
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-title', '-id')
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'),)

    def __str__(self):
        return f'{self.author}: {self.text[:33]}'

class Comment(models.Model):
     
    review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв')
    text = models.TextField(
        verbose_name='Текст комментария')
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментирования')

    class Meta:
        
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-review', '-id',)

    def __str__(self):
        return f'{self.author}: {self.text[:33]}'