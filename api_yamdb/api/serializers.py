from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.shortcuts import get_object_or_404
from reviews.models import (
    User, Comment, Review, Category, Genre, Title
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        lookup_field = 'slug'


class GenreField(serializers.Field):
    def to_representation(self, value):
        title_id = value.core_filters.get('title__id')
        title = Title.objects.get(pk=title_id)
        serializer = GenreSerializer(title.genre.all(), many=True)
        return serializer.data

    def to_internal_value(self, data):
        return data


class CategoryField(serializers.Field):
    def to_representation(self, value):
        serializer = CategorySerializer(value, many=False)
        return serializer.data

    def to_internal_value(self, data):
        return data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField()
    genre = GenreField()
    rating = serializers.SerializerMethodField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category',
        )
        model = Title

    def get_rating(self, obj):
        if not obj.reviews.exists():
            return None
        score_sum = 0
        for review in obj.reviews.all():
            score_sum += int(review.score)
        return (score_sum // obj.reviews.count())

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            title.genre.add(get_object_or_404(Genre, slug=genre))
        category_obj = get_object_or_404(Category, slug=category)
        category_obj.titles.add(title)
        return title

    def update(self, instance, validated_data):
        instance.genre.clear()
        if validated_data.get('name'):
            instance.name = validated_data.get('name')
        if validated_data.get('year'):
            instance.year = validated_data.get('year')
        if validated_data.get('description'):
            instance.description = validated_data.get('description')
        for genre in validated_data.get('genre'):
            instance.genre.add(get_object_or_404(Genre, slug=genre))
        instance.category = get_object_or_404(
            Category, slug=validated_data.get('category')
        )
        return instance
