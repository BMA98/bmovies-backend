from django_filters import rest_framework as filters

from history.models import MovieHistory


class MovieHistoryFilterSet(filters.FilterSet):

    class Meta:
        model = MovieHistory
        fields = {
            'timestamp': ['exact', 'year', 'year__gt', 'year__lt'],
            'movie_id': ['exact'],
        }
