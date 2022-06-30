from rest_framework import serializers
from movies.models import MovieRole


class StarRoleSerializer(serializers.ModelSerializer):
    """
    Serializes the many to many model MovieRole.
    Only fields star and role.
    """
    movie = serializers.SerializerMethodField()

    class Meta:
        model = MovieRole
        fields = ['movie', 'role']

    def get_movie(self, obj):
        from movies.serializers import MovieBasicSerializer
        return MovieBasicSerializer(obj.movie).data

