from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import MovieReview
from users.serializers import MovieReviewSerializer
from users.serializers.reviews import MovieReviewBasicSerializer


class MovieReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet intended to recover all ranks from an user.
    Authentication is required.
    """
    queryset = MovieReview.objects.all()
    serializers = {
        'get': MovieReviewSerializer,
        'list': MovieReviewSerializer,
        'create': MovieReviewBasicSerializer,
        'patch': MovieReviewBasicSerializer
    }
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthenticated,)
    filterset_fields = ['movie__tmdb_id']

    def get_queryset(self):
        print(f'Request: {self.request.data}')
        queryset = self.queryset
        query_set = queryset.filter(user_id=self.request.user.id)
        return query_set.order_by('id')

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializers['get']
        if self.action == 'retrieve':
            return self.serializers['list']
        if self.action == 'create':
            return self.serializers['create']
        if self.action == 'partial_update':
            return self.serializers['patch']
