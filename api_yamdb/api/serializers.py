from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    User, Comment, Review
)

from rest_framework.serializers import (
    CurrentUserDefault,
    ValidationError)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User
        validators = []


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')

class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True, default=CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('id', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title_id = (self.context['request'].path).split('/')[4]
        author = self.context['request'].user
        if Review.objects.values(
            'author', 'title').filter(
                author=author, title__id=title_id).exists():
            raise ValidationError('Вы уже написали отзыв.')
        return data
