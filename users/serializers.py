from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from movies.models import Movie
from movies.serializers import BasicMovieSerializer
from .models import User, MovieSeen, MovieRank, UserFavoriteMovie


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model, serializes all fields
    """
    favorites_movies = BasicMovieSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'


class UserRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True, max_length=255)
    lastname = serializers.CharField(required=True, max_length=255)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email_address_exists(email):
            raise serializers.ValidationError(
                "E-mail address is already in use.")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords didn't match.")
        return data

    def get_cleaned_data(self):
        return {
            'name': self.validated_data.get('name', ''),
            'lastname': self.validated_data.get('lastname', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }


class MovieSeenSerializer(serializers.ModelSerializer):
    """
    Serializer for MovieSeen model, serializes all fields
    """
    user = serializers.StringRelatedField()
    movie = BasicMovieSerializer()

    class Meta:
        model = MovieSeen
        fields = '__all__'


class MovieRankSerializer(serializers.ModelSerializer):
    """
    Serializer for MovieRank model, serializes all fields
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = MovieRank
        fields = '__all__'


class MovieDetailedRankSerializer(serializers.ModelSerializer):
    """
    Serializer for MovieRank model, serializes all fields
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    movie = BasicMovieSerializer()

    class Meta:
        model = MovieRank
        fields = '__all__'


class MovieOnlyRankSerializer(serializers.ModelSerializer):
    """
    Serializer for MovieRank model, serializes only movie and ranking
    """
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = MovieRank
        fields = ['movie', 'ranking']


class UserFavoriteMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFavoriteMovie
        fields = '__all__'


class UserFullFavoriteMovieSerializer(serializers.ModelSerializer):

    movie = BasicMovieSerializer()

    class Meta:
        model = UserFavoriteMovie
        fields = '__all__'


class UserLanguagesCountSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    language = serializers.CharField(source='movie__language')
    count = serializers.IntegerField()
