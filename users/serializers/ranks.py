from rest_framework import serializers

from movies.serializers import MovieSerializer
from users.models import MovieRank, User


class MovieRankSerializer(serializers.ModelSerializer):
    """
    Serializer for MovieRank model, serializes all fields
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    movie = MovieSerializer()

    class Meta:
        model = MovieRank
        fields = '__all__'


class MovieOnlyRankSerializer(serializers.ModelSerializer):
    """
    Serializer for MovieRank model, serializes only movie and ranking
    """
    movie = MovieSerializer()

    class Meta:
        model = MovieRank
        fields = ['movie', 'ranking']
