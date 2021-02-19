from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from movies.paginations import TenPageNumberPagination
from people.models import Star, Director, PhotographyDirector, ScreenWriter
from people.serializers import TopPeopleSerializer
from users.models import User, MovieSeen, MovieRank, UserFavoriteMovie
from users.serializers import MovieSeenSerializer, MovieRankSerializer, MovieOnlyRankSerializer, \
    UserFavoriteMovieSerializer, UserFullFavoriteMovieSerializer, MovieDetailedRankSerializer, UserSerializer


class MovieSeenViewSet(viewsets.ModelViewSet):
    """
    ViewSet intended to get all movies seen by a specific user.
    Authentication is required.
    """
    queryset = MovieSeen.objects.all()
    serializer_class = MovieSeenSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['movie__original_title']
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_fields = ['user', 'movie_id']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user_id=self.request.user.id)
        return query_set


class MovieRankViewSet(viewsets.ModelViewSet):
    """
    ViewSet intended to recover all ranks from an user.
    Authentication is required.
    """
    queryset = MovieRank.objects.all()
    serializer_class = MovieRankSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated,)
    filter_fields = ['movie__tmdb_id']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set

    def perform_update(self, serializer):
        serializer.save()


class MovieDetailedRankViewSet(viewsets.ModelViewSet):
    """
    ViewSet intended to recover all ranks from an user.
    Authentication is required.
    """
    queryset = MovieRank.objects.all()
    serializer_class = MovieDetailedRankSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['movie__original_title']
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_fields = ['movie__tmdb_id']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set

    def perform_update(self, serializer):
        serializer.save()


class MovieOnlyRankViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset intended to get all movie ranks, able to filter by movie.
    """
    queryset = MovieRank.objects.all()
    serializer_class = MovieOnlyRankSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['movie']


class UserFavoriteMovieViewSet(viewsets.ModelViewSet):
    """
    Viewset intended to get all favorite movies related to an user, able to filter by movie.
    Authentication is required.
    """
    queryset = UserFavoriteMovie.objects.all()
    serializer_class = UserFavoriteMovieSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['movie']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user_id=self.request.user.id)
        return query_set


class UserFullFavoriteMovieViewSet(viewsets.ModelViewSet):
    """
    Viewset intended to get all favorite movies related to an user, able to filter by movie.
    Authentication is required.
    """
    queryset = UserFavoriteMovie.objects.all()
    serializer_class = UserFullFavoriteMovieSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = TenPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['movie']
    search_fields = ['movie__original_title']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user_id=self.request.user.id)
        return query_set


class UsersViewSet(viewsets.ModelViewSet):
    """
    ViewSet intended to list all users information.
    Authentication and Admin Privileges are required.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    pagination_class = TenPageNumberPagination
    filter_backends = [DjangoFilterBackend, ]


class UserTopStars(viewsets.ModelViewSet):
    """
    ViewSet intended to return all stars sorted (descending) by their number of roles.
    If the user is authenticated, it returns values filtered for that particular user. Otherwise it uses global
    information.
    """
    pagination_class = TenPageNumberPagination
    queryset = Star.objects.all().prefetch_related()
    serializer_class = TopPeopleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        # If the user is authenticated, we filter their movies
        queryset = self.queryset
        if self.request.user.id:
            queryset = queryset.filter(movierole__movie__movieseen__user=self.request.user.id)
        # Counting movies
        queryset = queryset.annotate(movie_count=Count('movierole')).order_by('-movie_count', '-tmdb_id')
        return queryset


class UserTopDirectors(viewsets.ModelViewSet):
    """
    ViewSet intended to return all directors sorted (descending) by their number of movies.
    If the user is authenticated, it returns values filtered for that particular user. Otherwise it uses global
    information.
    """
    pagination_class = TenPageNumberPagination
    queryset = Director.objects.all().prefetch_related()
    serializer_class = TopPeopleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        # If the user is authenticated, we filter their movies
        queryset = self.queryset
        if self.request.user.id:
            queryset = queryset.filter(movie__movieseen__user=self.request.user.id)
        # Counting movies
        queryset = queryset.annotate(movie_count=Count('movie')).order_by('-movie_count', '-tmdb_id')
        return queryset


class UserTopPhotographyDirectors(viewsets.ModelViewSet):
    """
    ViewSet intended to return all directors sorted (descending) by their number of movies.
    If the user is authenticated, it returns values filtered for that particular user. Otherwise it uses global
    information.
    """
    pagination_class = TenPageNumberPagination
    queryset = PhotographyDirector.objects.all().prefetch_related()
    serializer_class = TopPeopleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        # If the user is authenticated, we filter their movies
        queryset = self.queryset
        if self.request.user.id:
            queryset = queryset.filter(movie__movieseen__user=self.request.user.id)
        # Counting movies
        queryset = queryset.annotate(movie_count=Count('movie')).order_by('-movie_count', '-tmdb_id')
        return queryset


class UserTopScreenwriters(viewsets.ModelViewSet):
    """
    ViewSet intended to return all directors sorted (descending) by their number of movies.
    If the user is authenticated, it returns values filtered for that particular user. Otherwise it uses global
    information.
    """
    pagination_class = TenPageNumberPagination
    queryset = ScreenWriter.objects.all().prefetch_related()
    serializer_class = TopPeopleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        # If the user is authenticated, we filter their movies
        queryset = self.queryset
        if self.request.user.id:
            queryset = queryset.filter(movie__movieseen__user=self.request.user.id)
        # Counting movies
        queryset = queryset.annotate(movie_count=Count('movie')).order_by('-movie_count', '-tmdb_id')
        return queryset
