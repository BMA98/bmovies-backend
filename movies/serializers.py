from rest_framework import serializers

from people.serializers import PeopleSerializer
from .models import Movie, Genre, Language, ProductionCountry


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ['language_iso']


class ProductionCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCountry
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):

    language = serializers.StringRelatedField()
    countries = serializers.StringRelatedField(many=True)
    genres = serializers.StringRelatedField(many=True)
    directors = PeopleSerializer(many=True)
    photography_directors = PeopleSerializer(many=True)
    screenwriters = PeopleSerializer(many=True)
    producers = PeopleSerializer(many=True)
    cast = PeopleSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

