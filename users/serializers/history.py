from rest_framework import serializers

from movies.serializers import MovieBasicSerializer
from users.models import MovieHistory


class MovieHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for MovieSeen model, serializes all fields
    """
    user = serializers.StringRelatedField()
    movie = MovieBasicSerializer()

    class Meta:
        model = MovieHistory
        fields = ['user', 'movie', 'timestamp', 'channel', 'created']


class MovieHistorySerializerBasic(serializers.ModelSerializer):

    class Meta:
        model = MovieHistory
        fields = ['user', 'movie', 'timestamp', 'channel', 'created']
