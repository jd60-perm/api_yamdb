from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import CurrentUserDefault, ValidationError
from reviews.models import Category, Comment, Genre, Review, Title, User


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


class TitleReadSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), many=False, slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field='slug'
    )
    description = serializers.CharField(required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
        model = Title

    def create(self, validated_data):
        category = validated_data.pop('category')
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            title.genre.add(genre)
        category.titles.add(title)
        return title

    def update(self, instance, validated_data):
        if validated_data.get('name'):
            instance.name = validated_data.get('name')
        if validated_data.get('year'):
            instance.year = validated_data.get('year')
        if validated_data.get('description'):
            instance.description = validated_data.get('description')
        if validated_data.get('genre'):
            instance.genre.clear()
            for genre in validated_data.get('genre'):
                instance.genre.add(genre)
        if validated_data.get('category'):
            instance.category.delete()
            instance.category = (validated_data.get('category'))
        instance.save()
        return instance


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=False)
    genre = GenreSerializer(read_only=True, many=True)
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
