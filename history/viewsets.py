from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from history.filtersets import MovieHistoryFilterSet
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
    permission_classes = (IsAuthenticated,)
    filterset_class = MovieHistoryFilterSet

    def get_queryset(self):
        queryset = self.queryset
        # distinct required for filtering and pagination to work along together
        print(self.request)
        queryset = queryset.distinct().filter(user=self.request.user)
        return queryset


class MovieHistoryUniqueViewSet(MovieHistoryViewSet):

    def get_queryset(self):
        queryset = super(MovieHistoryViewSet, self).get_queryset()
        return queryset.order_by('movie_id').distinct('movie_id')