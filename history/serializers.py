from rest_framework import serializers
from history.models import MovieHistory
from movies.serializers import BasicMovieSerializer


class MovieHistorySerializer(serializers.Serializer):

    movie = BasicMovieSerializer()
    user = serializers.StringRelatedField()
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S ")

    class Meta:
        model = MovieHistory
        fields = '__all__'
