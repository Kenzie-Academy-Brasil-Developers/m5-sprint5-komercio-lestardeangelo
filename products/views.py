from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .models import Product
from .serializers import ProductSerializerDetailed, ProductSerializerGeneral
from .permissions import IsProductOwner, IsSellerAndAuthenticated
from .mixins import SerializerByMethodMixin


class ProductView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerAndAuthenticated]

    queryset = Product.objects.all()
    serializer_map = {
        'GET': ProductSerializerGeneral,
        'POST': ProductSerializerDetailed,
    }
    
    def perform_create(self, serializer):
        seller = self.request.user
        serializer.save(seller=seller)


class ProductDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProductOwner]
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializerDetailed





