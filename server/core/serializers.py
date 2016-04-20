# Serializers define the API representation.
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

    class Meta:
        model = AppUser
        exclude = (
            'user_permissions', 'groups', 'is_active', 'is_staff', 'is_superuser', 'verified', 'unique_code', 'id'
        )


class RideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideRequest
