from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, SAFE_METHODS
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly
from .serializers import TitlesSerializerGet, TitlesSerializerPost, GenresSerializer, CategoriesSerializer
from .models import Title, Category, Genre

class CreateDelListViewset(CreateModelMixin, DestroyModelMixin,
                           ListModelMixin, GenericViewSet):
    pass


class CategoriesViewSet(CreateDelListViewset):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(CreateDelListViewset):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitlesViewset(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitlesSerializerGet
        return TitlesSerializerPost
