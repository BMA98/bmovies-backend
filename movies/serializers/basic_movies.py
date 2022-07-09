from rest_framework import serializers
from movies.models import Movie


class MovieBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['tmdb_id', 'original_title', 'year', 'release_date',
                  'runtime', 'overview', 'poster', 'backdrop', 'language', 'status']
