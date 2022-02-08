from rest_framework import serializers

from movies.models import Playlist, Collection, PlaylistRecord
from movies.models.playlists import CollectionRecord
from movies.serializers import MovieSerializer


class PlaylistRecordSerializer(serializers.ModelSerializer):

    movie = MovieSerializer()

    class Meta:
        model = PlaylistRecord
        fields = ['order', 'movie', 'description']


class PlaylistSerializer(serializers.ModelSerializer):

    movies = PlaylistRecordSerializer(source='playlistrecord_set', many=True)

    class Meta:
        model = Playlist
        fields = '__all__'


class CollectionRecordSerializer(serializers.ModelSerializer):
    playlist = PlaylistSerializer()

    class Meta:
        model = CollectionRecord
        fields = ['order', 'playlist']


class CollectionSerializer(serializers.ModelSerializer):

    playlists = CollectionRecordSerializer(source='collectionrecord_set', many=True)
    class Meta:
        model = Collection
        fields = '__all__'
