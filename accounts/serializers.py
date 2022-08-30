from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
        ]

        extra_kwargs = {"password": {"write_only": True}}

        read_only_fields = ["date_joined"]

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)


class AccountIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
        ]

        read_only_fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
        ]


class AccountIsActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
        ]

        read_only_fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
        ]


class UpdateAccountIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
        ]

        extra_kwargs = {"password": {"write_only": True}}

        read_only_fields = [
            "id",
            "date_joined",
            "is_active",
        ]

    def validate_password(self, password: str):
        password = make_password(password)

        return password


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(source="username")
    password = serializers.CharField()
