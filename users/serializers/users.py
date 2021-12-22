from rest_framework import serializers

from movies.serializers import MovieSerializer
from users.models import User

from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.utils import email_address_exists


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model, serializes all fields
    """
    favorites_movies = MovieSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'lastname', 'active', 'staff', 'admin',
                  'movie_history', 'favorites_movies', 'url_tokens']


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
