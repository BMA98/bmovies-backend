from rest_framework import serializers
from movies.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    """
    It serializes the Genre model.
    All fields.
    """
    class Meta:
        model = Genre
        fields = '__all__'

