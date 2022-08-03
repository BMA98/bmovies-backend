from rest_framework import serializers

from movies.serializers import MovieBasicSerializer
from users.models import MovieRank, User


class MovieReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for MovieRank model, serializes all fields
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    movie = MovieBasicSerializer()

    class Meta:
        model = MovieRank
        fields = '__all__'


class MovieReviewBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieRank
        fields = ['id', 'user', 'movie', 'ranking']