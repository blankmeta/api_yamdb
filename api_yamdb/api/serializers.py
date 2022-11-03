from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, Review, Rating, Comment


class CategorySerializer(serializers.Model):
    
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelField):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    # genre = 
 

class ReviewSerializer(serializers.ModelSerializer):
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
            raise serializers.ValidationError('Вы уже оставляли отзыв')
        return data



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
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('title',)