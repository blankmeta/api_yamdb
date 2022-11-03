from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from reviews.models import Review, Rating, Comment
from reviews.models import Title
from users.permissions import IsAuthor
from .serializers import ReviewSerializer


# Create your views here.
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user,
                        title=title)


class RatingViewSet(viewsets.ModelViewSet):
    pass