from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from categories.models import Category, Genre, Title
from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
    )


    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'rating', 'pub_date',)
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(), fields=('author', 'title'),
            ),
        )


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Genre.objects.all(),
        many=True,
        required=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
        required=True,
    )
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category', 'rating')