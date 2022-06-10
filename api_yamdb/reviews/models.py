from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    USER_ROLES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    ]

    email = models.EmailField(
        'Адрес почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    role = models.CharField(
        'Роль пользователя',
        choices=USER_ROLES,
        default='user',
        max_length=20,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=20,
    )

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER_ROLES[0][1]

    @property
    def is_moderator(self):
        return self.role == self.USER_ROLES[1][1]

    @property
    def is_admin(self):
        return self.role == self.USER_ROLES[2][1] or self.is_superuser


class Category(models.Model):
    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Наименование',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-id',)

    def __str__(self):
        return self.name[:15]


class Genre(models.Model):
    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Наименование',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-id',)

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.TextField(
        verbose_name='Наименование',
    )
    year = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(
                limit_value=date.today().year,
                message='Title\'s year can not be greater than current year',
            )
        ],
        verbose_name='Год выпуска',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )
    description = models.TextField(
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-id',)

    def __str__(self):
        return self.name[:15]


class Review(models.Model):

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
    score = models.PositiveSmallIntegerField(
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
