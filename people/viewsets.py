from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import People
from .serializers import PeopleSerializer


class PeopleViewSet(viewsets.ModelViewSet):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tmdb_id']