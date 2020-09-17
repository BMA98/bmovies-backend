from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from users.models import User, MovieSeen, MovieRank, UserFavoriteMovie
from users.serializers import MovieSeenSerializer, MovieRankSerializer, MovieOnlyRankSerializer, \
    UserFavoriteMovieSerializer, UserFullFavoriteMovieSerializer, MovieDetailedRankSerializer


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
    pagination_class.page_size = 25
    filter_fields = ['user']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
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
    pagination_class.page_size = 100
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
    pagination_class = PageNumberPagination
    pagination_class.page_size = 25
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['movie']
    search_fields = ['movie__original_title']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user_id=self.request.user.id)
        return query_set

