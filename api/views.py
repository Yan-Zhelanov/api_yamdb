from django.db.models import Avg
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .filters import TitleFilter
from .models import Title, Genre, Category
from .permissions import ReadOnly, IsAdmin
from .serializers import (TitlesSerializerGet, TitlesSerializerPost,
                          GenresSerializer, CategoriesSerializer)

class CreateDelListViewset(CreateModelMixin, DestroyModelMixin,
                           ListModelMixin, GenericViewSet):
    pass


class CategoriesViewSet(CreateDelListViewset):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdmin|ReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(CreateDelListViewset):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdmin|ReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitlesViewset(ModelViewSet):
    permission_classes = (IsAdmin|ReadOnly,)
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitlesSerializerGet
        return TitlesSerializerPost
