from rest_framework import serializers
from .models import Movie, Genre, Language


class MovieSerializer(serializers.ModelSerializer):

    language = serializers.StringRelatedField()
    genres = serializers.StringRelatedField(many=True)
    director = serializers.StringRelatedField(many=True)
    photography_director = serializers.StringRelatedField(many=True)
    screenwriter = serializers.StringRelatedField(many=True)
    producer = serializers.StringRelatedField(many=True)
    cast = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'
