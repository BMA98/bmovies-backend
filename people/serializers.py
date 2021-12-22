from rest_framework import serializers
from .models import Star, People
from drf_writable_nested.mixins import UniqueFieldsMixin


class StarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Star
        fields = '__all__'


class PeopleSerializer(UniqueFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = People
        fields = '__all__'