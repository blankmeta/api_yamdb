from statistics import mean

from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404

from reviews.models import Review, Title, Category, Genre
from users.permissions import AuthorOrReadOnly, AdminOrSuperUser
from .serializers import (ReviewSerializer, CommentSerializer,
                          CategorySerializer, GenreSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [AdminOrSuperUser, AuthorOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [AdminOrSuperUser, AuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [AdminOrSuperUser, AuthorOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly, AdminOrSuperUser,)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user,
                        title=title)


# class RatingViewSet(viewsets.ModelViewSet):
#     serializer_class = RatingSerializer
#     permission_classes = (AuthorOrReadOnly,)

#     def get_queryset(self):
#         title_id = self.kwargs['title_id']
#         title = get_object_or_404(Title, pk=title_id)
#         estimations = title.rating.all()
#         rate_avg = mean(estimations)
#         return rate_avg

#     def perform_create(self, serializer):
#         title_id = self.kwargs['title_id']
#         title = get_object_or_404(Title, pk=title_id)
#         serializer.save(author=self.request.user,
#                         title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly, AdminOrSuperUser,)

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user,
                        review=review)

