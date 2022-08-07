from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from movies.paginations import TenPageNumberPagination
from movies.serializers import MovieSerializer, GenreSerializer
from movies.models import Movie, Genre
from movies.serializers.movies import TheMovieDBSerializer
from movies.themoviedb import update_or_create_movie


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
    filterset_fields = ['tmdb_id', 'year', 'genres', 'genres__name', 'language']


class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Genre model.
    It allows filter by id.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['genre_id']


class MovieInsertViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated, IsAdminUser, )

    def create(self, request):
        print(request.data)
        movie = update_or_create_movie(**request.data)
        return Response(MovieSerializer(movie).data)

