from core.mixins import SerializerByMethodMixin
from rest_framework import authentication, generics

from .models import Product
from .permissions import (IsAuthenticatedOwnerSellerPermission,
                          IsAuthenticatedSellerPermission)
from .serializers import ProductCreateSerializer, ProductListSerializer


class ProductsView(SerializerByMethodMixin, generics.ListCreateAPIView):

    queryset = Product.objects.all()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticatedSellerPermission]

    serializer_map = {
        "GET": ProductListSerializer,
        "POST": ProductCreateSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductIdView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):

    queryset = Product.objects.all()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticatedOwnerSellerPermission]

    serializer_map = {
        "GET": ProductListSerializer,
        "PATCH": ProductCreateSerializer,
    }
