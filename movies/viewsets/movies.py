from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


from movies.paginations import TenPageNumberPagination
from movies.serializers import MovieSerializer, GenreSerializer
from movies.models import Movie, Genre


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Movie model.
    It allows search by original_title.
    It allows filters by genre, year or people involved in cast, directing, screenwriting or photography.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,]
    search_fields = ['original_title']
    pagination_class = TenPageNumberPagination
    filter_fields = [
                     'year', 'genres', 'genres__name', 'language']


class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Genre model.
    It allows filter by id.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['genre_id']
