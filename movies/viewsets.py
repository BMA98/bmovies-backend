from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Movie, Genre, Language
from .serializers import MovieSerializer, GenreSerializer, LanguageSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,]
    search_fields = ['original_title']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 25
    filter_fields = ['cast__tmdb_id', 'directors__tmdb_id', 'screenwriters__tmdb_id', 'photography_directors__tmdb_id', 'year', 'genres']


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['genre_id']


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['language_id']