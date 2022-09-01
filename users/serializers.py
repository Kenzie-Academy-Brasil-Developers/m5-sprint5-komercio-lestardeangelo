from rest_framework import serializers
from .models import Account
from rest_framework.exceptions import APIException


class UniqueValidationError(APIException):
    status_code = 422


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'is_seller', 'date_joined', 'is_active', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

        
    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user
    