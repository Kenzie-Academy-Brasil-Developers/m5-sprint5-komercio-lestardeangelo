from rest_framework import serializers
from users.models import User


class UserSerializerID(serializers.ModelSerializer):
    class Meta:

        model = User

        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
        }

        read_only_fields = ["date_joined"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:

        model = User

        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
        }

        read_only_fields = ["date_joined"]

    def create(self, validated_data: dict):

        user = User.objects.create_user(**validated_data)

        return user

    def update(self, instance, validated_data: dict):
        is_seller = validated_data.pop("is_seller", False)

        user = User.objects.update_user(instance, **validated_data)

        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)


class UserManageAdminSerializer(serializers.ModelSerializer):
    class Meta:

        model = User

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
            "email",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "date_joined",
        ]
