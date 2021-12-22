from rest_framework import serializers

from movies.serializers import MovieSerializer
from users.models import UserFavoriteMovie


class UserFavoriteMovieSerializer(serializers.ModelSerializer):

    movie = MovieSerializer()

    class Meta:
        model = UserFavoriteMovie
        fields = '__all__'
