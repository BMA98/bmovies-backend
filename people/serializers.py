from rest_framework import serializers
from .models import Star, People


class StarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Star
        fields = '__all__'


class PeopleSerializer(serializers.ModelSerializer):

    class Meta:
        model = People
        fields = '__all__'