from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import User, MovieSeen, MovieRank
from users.serializers import MovieSeenSerializer, MovieRankSerializer, MovieOnlyRankSerializer, \
    UserFavoriteMovieSerializer


class MovieSeenViewSet(viewsets.ModelViewSet):
    """
    ViewSet intended to get all movies seen by a specific user.
    Authentication is required.
    """
    queryset = MovieSeen.objects.all()
    serializer_class = MovieSeenSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated,)
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
    filter_fields = ['movie']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set

    def perform_update(self, serializer):
        serializer.save()


class MovieOnlyRankViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Serializer intended to get all movie ranks, able to filter by movie.
    """
    queryset = MovieRank.objects.all()
    serializer_class = MovieOnlyRankSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['movie']


class UserFavoriteMovieViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserFavoriteMovieSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['favorites_movies']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(id=self.request.user.id)
        return query_set

    def perform_update(self, serializer):
        serializer.save()
