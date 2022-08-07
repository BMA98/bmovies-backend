from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from movies.models import Movie, MovieRole
from movies.serializers import GenreSerializer, MovieRoleSerializer, TrackSerializer
from people.models import People
from people.serializers import PeopleBasicSerializer


class MovieSerializer(WritableNestedModelSerializer):

    """
    Serializes the Movie model.
    All fields, using nested serializers.
    """
    genres = GenreSerializer(many=True, required=False)
    directors = PeopleBasicSerializer(many=True, required=False)
    photography_directors = PeopleBasicSerializer(many=True, required=False)
    screenwriters = PeopleBasicSerializer(many=True, required=False)
    cast = MovieRoleSerializer(source='movierole_set', many=True, required=False)
    songs = TrackSerializer(many=True, required=False)

    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        # Check whether there are incoming cast members
        if 'movierole_set' in validated_data:
            cast = validated_data.pop('movierole_set')
        else:
            cast = []
        movie, created = Movie.objects.get_or_create(tmdb_id=validated_data.pop('tmdb_id'), **validated_data)
        for role in cast:
            star = role.pop('star')
            tmdb_id = star.pop('tmdb_id')
            star, _ = People.objects.get_or_create(tmdb_id=tmdb_id, defaults=star)
            star.save()
            role, _ = MovieRole.objects.get_or_create(movie=movie, star=star, role=role['role'])
        movie.save()
        return movie


class TheMovieDBSerializer(serializers.Serializer):

    tmdb_id = serializers.IntegerField()
    status = serializers.IntegerField(required=False, default=0)
    trailer = serializers.IntegerField(required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
