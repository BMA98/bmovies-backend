from rest_framework import serializers

from people.serializers import PeopleSerializer
from .models import Movie, Genre, Language, ProductionCountry, MovieRole, Song, MovieSong


class SongSerializer(serializers.ModelSerializer):
    """
    Serializes Song model.
    All fields.
    """
    class Meta:
        model = Song
        fields = '__all__'


class MovieSongSerializer(serializers.ModelSerializer):
    """
    Serializes the many to many model MovieSong.
    Only fields song and order.
    """
    song = SongSerializer()
    order = serializers.IntegerField()

    class Meta:
        model = MovieSong
        fields = ['song', 'order']


class LanguageSerializer(serializers.ModelSerializer):
    """
    Serializes the Language model.
    """
    class Meta:
        model = Language
        fields = ['language_iso']


class ProductionCountrySerializer(serializers.ModelSerializer):
    """
    Serializes the ProductionContry Model.
    All fields.
    """
    class Meta:
        model = ProductionCountry
        fields = '__all__'


class MovieRoleSerializer(serializers.ModelSerializer):
    """
    Serializes the many to many model MovieRole.
    Only fields star and role.
    """
    #movie = serializers.Field(source='cast.movie.tmdb_id')
    star = PeopleSerializer()
    role = serializers.CharField()

    class Meta:
        model = MovieRole
        fields = ['star', 'role']


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializes the Movie model.
    All fields, using nested serializers.
    """
    language = serializers.StringRelatedField()
    countries = serializers.StringRelatedField(many=True)
    genres = serializers.StringRelatedField(many=True)
    directors = PeopleSerializer(many=True)
    photography_directors = PeopleSerializer(many=True)
    screenwriters = PeopleSerializer(many=True)
    producers = PeopleSerializer(many=True)
    cast = MovieRoleSerializer(source='movierole_set', many=True)
    songs = SongSerializer()

    class Meta:
        model = Movie
        fields = '__all__'


class BasicMovieSerializer(serializers.ModelSerializer):
    """
    It serializes the Movie model.
    Only fields tmdb_id, original_title, title, year, overview, poster and backdrop.
    It doesn't use nested serializers.
    """
    class Meta:
        model = Movie
        fields = ['tmdb_id', 'original_title', 'title', 'year', 'overview', 'poster', 'backdrop']


class GenreSerializer(serializers.ModelSerializer):
    """
    It serializes the Genre model.
    All fields.
    """
    class Meta:
        model = Genre
        fields = '__all__'

