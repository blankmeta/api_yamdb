from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.Model):
    
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelField):

    class Meta:
        model = Genre
        fields = '__all__'
