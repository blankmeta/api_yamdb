from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .fields import CategorySlugRelatedField, GenreSlugRelatedField
from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField('get_rating')
    category = CategorySlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    genre = GenreSlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get(
            'score__avg')
        if not rating:
            return rating
        return round(rating, 1)


class ReviewSerializer(serializers.ModelSerializer):
    # id = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username',
                                          default=(serializers
                                                   .CurrentUserDefault()))

    class Meta:
        fields = ('id', 'title', 'author', 'text', 'created', 'score',)
        model = Review
        read_only_fields = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author',)
            )
        ]

    # def validate(self, data):
    #     if Review.objects.filter(title=get_object_or_404(Title, id=self.kwargs['title_id'])):
    #         raise serializers.ValidationError('Вы уже оставляли отзыв')
    #     return data


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author',)
            )
        ]

    def validate(self, data):
        if data['author'] == self.context.get('request').user:
            raise serializers.ValidationError('Вы уже оценили произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username',
                                          default=serializers.CurrentUserDefault())

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
