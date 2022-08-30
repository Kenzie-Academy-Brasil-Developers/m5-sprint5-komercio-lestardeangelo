from django.db import IntegrityError
from accounts.models import Account
from core.mixins import SerializerByMethodMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import Response, status

from products.models import Product
from products.permissions import IsSeller
from products.serializers import CreateProductSerializer, ListProductSerializer


class ProductView(SerializerByMethodMixin, ListCreateAPIView):
    queryset = Product.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSeller]

    serializer_map = {
        "GET": ListProductSerializer,
        "POST": CreateProductSerializer,
    }

    def perform_create(self, serializer: CreateProductSerializer):
        serializer.save(seller=self.request.user)


class ProductIdView(SerializerByMethodMixin, RetrieveUpdateAPIView):
    queryset = Product.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSeller]

    serializer_map = {
        "GET": ListProductSerializer,
        "PATCH": CreateProductSerializer,
    }
