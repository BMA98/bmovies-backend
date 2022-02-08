from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from movies.models import Playlist, Collection
from movies.paginations import TenPageNumberPagination
from movies.serializers import PlaylistSerializer, CollectionSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, ]
    search_fields = ['name']
    pagination_class = TenPageNumberPagination
    filter_fields = ['id', 'name']


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, ]
    search_fields = ['name']
    pagination_class = TenPageNumberPagination
    filter_fields = ['id', 'name']
