from rest_framework import serializers
from .models import Star, People


class StarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Star
        fields = '__all__'


class TopPeopleSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    tmdb_id = serializers.IntegerField()
    imdb_id = serializers.CharField()
    name = serializers.CharField()
    biography = serializers.CharField()
    gender = serializers.IntegerField()
    profile_path = serializers.CharField()
    birthday = serializers.DateField()
    birthplace = serializers.CharField()
    deathday = serializers.DateField()
    movie_count = serializers.IntegerField()


class PeopleSerializer(serializers.ModelSerializer):

    class Meta:
        model = People
        fields = '__all__'