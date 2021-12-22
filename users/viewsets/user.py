from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from movies.paginations import TenPageNumberPagination
from users.models import User
from users.serializers.users import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """
    ViewSet intended to list all users information.
    Authentication and Admin Privileges are required.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = TenPageNumberPagination
    filter_backends = [DjangoFilterBackend, ]

    def get_queryset(self):
        # If the user has admin privileges
        if self.request.user.is_admin:
            # In case the admin user is requesting all users
            if 'all' in self.request.query_params:
                return self.queryset
        # Otherwise, just returns info of the current user
        return self.queryset.filter(id=self.request.user.id)
