from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

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
    filter_backends = [DjangoFilterBackend, SearchFilter,]
    search_fields = ['movie__original_title']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 25
    permission_classes = (IsAuthenticated,)
    filter_fields = ['user', 'movie__tmdb_id', 'movie__year', 'timestamp']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set
