from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from movies.models import Movie, MovieRole
from people.models import Star
from people.serializers import PeopleSerializer
from movies.serializers import GenreSerializer, MovieRoleSerializer


class MovieSerializer(WritableNestedModelSerializer):

    """
    Serializes the Movie model.
    All fields, using nested serializers.
    """
    genres = GenreSerializer(many=True, required=False)
    directors = PeopleSerializer(many=True, required=False)
    photography_directors = PeopleSerializer(many=True, required=False)
    screenwriters = PeopleSerializer(many=True, required=False)
    cast = MovieRoleSerializer(source='movierole_set', many=True, required=False)
    #songs = TrackSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        cast = validated_data.pop('movierole_set')
        print(validated_data)
        movie, created = Movie.objects.get_or_create(tmdb_id=validated_data.pop('tmdb_id'), **validated_data)
        for role in cast:
            star = role.pop('star')
            tmdb_id = star.pop('tmdb_id')
            star, _ = Star.objects.get_or_create(tmdb_id=tmdb_id, defaults=star)
            star.save()
            role, _ = MovieRole.objects.get_or_create(movie=movie, star=star, role=role['role'])
            #movie.cast(role)
        movie.save()
        return movie

