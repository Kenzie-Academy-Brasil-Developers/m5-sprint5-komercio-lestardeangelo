from rest_framework import serializers
from accounts.serializers import AccountIdSerializer, AccountSerializer

from products.models import Product


class CreateProductSerializer(serializers.ModelSerializer):
    seller = AccountIdSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "description",
            "price",
            "quantity",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "is_active",
        ]


class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]

        read_only_fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]
