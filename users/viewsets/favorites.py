from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import UserFavoriteMovie
from users.serializers import UserFavoriteMovieSerializer


class UserFavoriteMovieViewSet(viewsets.ModelViewSet):
    """
    Viewset intended to get all favorite movies related to an user, able to filter by movie.
    Authentication is required.
    """
    queryset = UserFavoriteMovie.objects.all()
    serializer_class = UserFavoriteMovieSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user_id=self.request.user.id)
        return query_set
