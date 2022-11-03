from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.Model):
    
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelField):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField('get_rating')
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('estimate ')).get('estimate__avg')
        if not rating:
            return rating
        return round(rating, 1)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username',
                                          default=(serializers
                                                   .CurrentUserDefault()))

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]

    def validate(self, data):
        if data['author'] == self.context.get('request').user:
            raise serializers.ValidationError('Вы уже оставляли отзыв')
        return data


# class RatingSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(read_only=True,
#                                           slug_field='username')

#     class Meta:
#         fields = '__all__'
#         model = Review
#         read_only_fields = ('title',)
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Review.objects.all(),
#                 fields=('author', 'title')
#             )
#         ]

#     def validate(self, data):
#         if data['author'] == self.context.get('request').user:
#             raise serializers.ValidationError('Вы уже оценили произведение')
#         return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('title',)


