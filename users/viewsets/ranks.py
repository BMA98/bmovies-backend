from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import MovieRank
from users.serializers import MovieRankSerializer, MovieOnlyRankSerializer


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


class MovieOnlyRankViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset intended to get all movie ranks, able to filter by movie.
    """
    queryset = MovieRank.objects.all()
    serializer_class = MovieOnlyRankSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['movie']
