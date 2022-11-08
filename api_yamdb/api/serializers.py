from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment
from .fields import CategorySlugRelatedField, GenreSlugRelatedField


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
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username',
                                          default=(serializers
                                                   .CurrentUserDefault()))

    class Meta:
        fields = ('id', 'title', 'author', 'text', 'pub_date', 'score',)
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        request = self.context['request']
        title = get_object_or_404(Title,
                                  id=self.context.get("view").kwargs.get(
                                      "title_id"))
        if request.method == 'POST':
            if Review.objects.filter(title=title,
                                     author=request.user).exists():
                raise serializers.ValidationError('Вы уже оставляли отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
