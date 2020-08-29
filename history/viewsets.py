from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from history.models import MovieHistory
from history.serializers import MovieHistorySerializer
from rest_framework.permissions import IsAuthenticated


class MovieHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet intended to recover all viewing entries for a particular user.
    Newer entries come first.
    Authentication is required.
    """
    queryset = MovieHistory.objects.all().order_by('-timestamp')
    serializer_class = MovieHistorySerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated,)
    filter_fields = ['user']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set
