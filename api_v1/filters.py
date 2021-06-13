from django_filters import rest_framework as filters

from .models import Title


class TitleFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    genre = filters.CharFilter(field_name='genre_slug')
    category = filters.CharFilter(field_name='category_slug')

    class Meta:
        model = Title
        fields = ('name', 'genre', 'category', 'year',)
