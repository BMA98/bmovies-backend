from rest_framework import serializers

from people.models import People
from movies.serializers import MovieBasicSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin


class PeopleSerializer(UniqueFieldsMixin, serializers.ModelSerializer):

    cast_roles = serializers.SerializerMethodField()
    director_roles = MovieBasicSerializer(many=True, required=False)
    screenwriter_roles = MovieBasicSerializer(many=True, required=False)
    photography_roles = MovieBasicSerializer(many=True, required=False)

    class Meta:
        model = People
        fields = '__all__'

    def get_cast_roles(self, obj):
        from movies.serializers import StarRoleSerializer
        roles = obj.movierole_set.all()
        print(roles)
        return StarRoleSerializer(roles, many=True).data


class PeopleBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = People
        fields = '__all__'
