from django_filters import rest_framework as filters

from users.models import MovieHistory


class MovieHistoryFilterSet(filters.FilterSet):

    class Meta:
        model = MovieHistory
        fields = {
            'user': ['exact'],
            'timestamp': ['exact', 'year', 'year__gt', 'year__lt'],
            'movie_id': ['exact', 'in'],
            'movie__language': ['exact'],
        }