from rest_framework import serializers
from movies.models import Track


class TrackSerializer(serializers.ModelSerializer):
    """
    Serializes Track model.
    All fields.
    """
    class Meta:
        model = Track
        fields = '__all__'
