from rest_framework import serializers

from movies.serializers import GenreSerializer
from people.serializers import PeopleSerializer
from series.models import Network, SeriesRole, Episode, Season, Series


class SeriesRoleSerializer(serializers.ModelSerializer):

    star = PeopleSerializer()
    role = serializers.CharField()

    class Meta:
        model = SeriesRole
        fields = ['star', 'role']


class EpisodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Episode
        fields = '__all__'


class SeasonSerializer(serializers.ModelSerializer):

    episodes = EpisodeSerializer(many=True)

    class Meta:
        model = Season
        fields = '__all__'


class SeriesSerializer(serializers.ModelSerializer):

    seasons = SeasonSerializer(many=True)
    created_by = PeopleSerializer(many=True)
    cast = SeriesRoleSerializer(source='seriesrole_set', many=True)
    language = serializers.StringRelatedField()
    countries = serializers.StringRelatedField(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Series
        fields = '__all__'


class NetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network
        fields = '__all__'
