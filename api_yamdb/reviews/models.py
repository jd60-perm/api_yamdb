from django.core.validators import (
    MaxValueValidator, MinValueValidator
)
from django.db import models

#from users.models import User



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