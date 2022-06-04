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
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
    )
    description = models.TextField()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name[:15]


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                limit_value=1,
                message='The score can\'t be less than 1'
            ),
            MaxValueValidator(
                limit_value=10,
                message='The score can\'t be greater than 10'
            )
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.text[:15]

