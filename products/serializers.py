from rest_framework import serializers

from .models import Product
from users.serializers import AccountSerializer


class ProductSerializerDetailed(serializers.ModelSerializer):
    seller = AccountSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id','seller', 'description', 'price', 'quantity', 'is_active']


class ProductSerializerGeneral(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['description', 'price', 'quantity', 'is_active', 'seller_id']
        read_only_fields = ['description', 'price', 'quantity', 'is_active', 'seller_id']
        