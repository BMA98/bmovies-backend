from rest_framework import serializers

from movies.models import Movie
from users.serializers import UserSerializer


class MovieCountSerializer(serializers.Serializer):

    language = serializers.CharField()
    language_count = serializers.IntegerField()
