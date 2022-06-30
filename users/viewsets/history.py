from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from movies.paginations import TenPageNumberPagination
from users.filtersets import MovieHistoryFilterSet
from users.models import MovieHistory
from users.serializers import MovieHistorySerializer, MovieHistorySerializerBasic


class MovieHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet intended to get all movies seen by a specific user.
    Authentication is required.
    """
    queryset = MovieHistory.objects.all()
    serializers = {
        'list': MovieHistorySerializer,
        'create': MovieHistorySerializerBasic
    }
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['movie__original_title']
    permission_classes = (IsAuthenticated,)
    filterset_class = MovieHistoryFilterSet

    def get_queryset(self):
        queryset = self.queryset
        print(f'user {self.request.user.id}')
        query_set = queryset.filter(user_id=self.request.user.id).order_by('-timestamp')
        return query_set

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializers['list']
        if self.action == 'create':
            return self.serializers['create']