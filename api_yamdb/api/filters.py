import requests
from rest_framework import filters

from reviews.models import Genre, Category, Title


class TitleFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request: requests.request, queryset, view):
        category_slug = request.query_params.get('category')
        genre_slug = request.query_params.get('genre')
        name = request.query_params.get('name')
        year = request.query_params.get('year')

        if Genre.objects.filter(slug=genre_slug):
            genre_id = Genre.objects.get(slug=genre_slug).id
            queryset = queryset.filter(genre=genre_id)
        if Category.objects.filter(slug=category_slug):
            category_id = Category.objects.get(slug=category_slug).id
            queryset = queryset.filter(category=category_id)
        if queryset.filter(year=year):
            queryset = queryset.filter(year=year)
        if name:
            if Title.objects.filter(name__in=self.get_names(name)):
                queryset = queryset.filter(name__in=self.get_names(name))

        return queryset

    @staticmethod
    def get_names(name):
        return [title.name for title in Title.objects.all() if
                name in title.name]
