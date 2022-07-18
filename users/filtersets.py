import django_filters
from django_filters import rest_framework as filters

from users.models import MovieHistory


class MovieHistoryFilterSet(filters.FilterSet):

    language = filters.CharFilter(field_name='movie__language', lookup_expr='exact')
    tmdb_id = filters.NumberFilter(field_name='movie_id', lookup_expr='exact')

    class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
        pass

    tmdb_id__in = NumberInFilter(field_name='movie_id', lookup_expr='in')

    class Meta:
        model = MovieHistory
        fields = {
            'user': ['exact'],
            'timestamp': ['exact', 'year', 'year__gt', 'year__lt']
        }