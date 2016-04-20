# Serializers define the API representation.
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import AppUser, RideRequest


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = ('url', 'username', 'email', 'is_staff')


class CreateUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key

    def create(self, validated_data):
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data['password'])
        user = get_user_model().objects.create(**validated_data)
        return user

    class Meta:
        model = AppUser
        exclude = (
            'user_permissions', 'groups', 'is_active', 'is_staff', 'is_superuser', 'verified', 'unique_code', 'id'
        )
        write_only_fields = ('password', )


class RideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideRequest
