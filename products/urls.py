from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductView.as_view(), name="product-view"),
    path('products/<pk>/', views.ProductDetailView.as_view(), name="product-detail"),
]