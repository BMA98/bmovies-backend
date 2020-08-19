from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Star, People
from .serializers import StarSerializer, PeopleSerializer


class StarViewSet(viewsets.ModelViewSet):
    queryset = Star.objects.all()
    serializer_class = StarSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['tmdb_id']


class PeopleViewSet(viewsets.ModelViewSet):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['tmdb_id']