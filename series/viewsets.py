from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from series.models import Series, Season
from series.serializers import SeriesSerializer, SeasonSerializer


class SeriesViewsSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, ]
    search_fields = ['original_title']
    pagination_class = PageNumberPagination
    filter_fields = ['cast__tmdb_id', 'genres']


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    filter_backends = [DjangoFilterBackend, ]
    pagination_class = PageNumberPagination
    filter_fields = []