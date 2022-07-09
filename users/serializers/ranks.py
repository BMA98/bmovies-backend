from rest_framework import serializers

from movies.serializers import MovieSerializer, MovieBasicSerializer
from users.models import MovieRank, User


class MovieRankSerializer(serializers.ModelSerializer):
    """
    Serializer for MovieRank model, serializes all fields
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    movie = MovieBasicSerializer()

    class Meta:
        model = MovieRank
        fields = '__all__'


class MovieRankBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieRank
        fields = ['id', 'user', 'movie', 'ranking']
