from rest_framework import serializers

from users.models import URLToken


class URLTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for MovieRank model, serializes all fields
    """

    class Meta:
        model = URLToken
        fields = ['token', 'created', 'description']