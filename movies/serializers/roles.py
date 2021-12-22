from rest_framework import serializers
from movies.models import MovieRole
from people.serializers import PeopleSerializer


class MovieRoleSerializer(serializers.ModelSerializer):
    """
    Serializes the many to many model MovieRole.
    Only fields star and role.
    """
    star = PeopleSerializer()
    role = serializers.CharField()

    class Meta:
        model = MovieRole
        fields = ['star', 'role']
