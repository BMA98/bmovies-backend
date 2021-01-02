from rest_framework import serializers
from history.models import MovieHistory
from movies.serializers import MovieSerializer


class MovieHistorySerializer(serializers.Serializer):

    movie = MovieSerializer()
    user = serializers.StringRelatedField()
    channel = serializers.StringRelatedField()
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = MovieHistory
        fields = '__all__'


class MovieHistoryUniqueSerializer(serializers.Serializer):

    movie_id = serializers.IntegerField()