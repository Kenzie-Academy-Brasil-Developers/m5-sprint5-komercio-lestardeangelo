from rest_framework import serializers

from products.models import Product
from users.models import User


class SellerSerializer(serializers.ModelSerializer):
    class Meta:

        model = User

        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
        ]


class ProductCreateSerializer(serializers.ModelSerializer):

    seller = SellerSerializer(read_only=True, source="user")
    id = serializers.UUIDField(read_only=True, source="product_uuid")

    class Meta:

        model = Product

        fields = ["id", "description", "price", "quantity", "is_active", "seller"]

        extra_kwargs = {"quantity": {"min_value": 0}}


class ProductListSerializer(serializers.ModelSerializer):

    seller_id = serializers.UUIDField(source="user.id")

    class Meta:

        model = Product

        fields = (
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        )
