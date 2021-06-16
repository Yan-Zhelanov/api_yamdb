from django import db, shortcuts
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import throttling, viewsets
from rest_framework.pagination import CursorPagination

from .models import Title
from .permissions import (IsAdminOrReadOnly, IsAuthorOrReadOnly,
                          IsModeratorOrReadOnly)
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = CursorPagination
    permission_classes = [IsAdminOrReadOnly,
                          IsAuthorOrReadOnly,
                          IsModeratorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    throttle_classes = [throttling.UserRateThrottle,
                        throttling.AnonRateThrottle]

    def get_title(self):
        return shortcuts.get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title
        )
        self.get_title().save(rating=self.get_object().aggregate(
            db.models.Avg('score')
        ))

    def perform_update(self, serializer):
        serializer.save()
        self.get_title().save(rating=self.get_object().aggregate(
            db.models.Avg('score')
        ))


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = CursorPagination
    permission_classes = [IsAdminOrReadOnly,
                          IsAuthorOrReadOnly,
                          IsModeratorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    throttle_classes = [throttling.UserRateThrottle,
                        throttling.AnonRateThrottle]

    def get_review(self):
        title = shortcuts.get_object_or_404(Title, id=self.kwargs['title_id'])
        return shortcuts.get_object_or_404(title.reviews,
                                           id=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review
        )
