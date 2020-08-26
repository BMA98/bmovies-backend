from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

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

    def get_cleaned_data(self):
        return {
            'name': self.validated_data.get('name', ''),
            'lastname': self.validated_data.get('lastname', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user
