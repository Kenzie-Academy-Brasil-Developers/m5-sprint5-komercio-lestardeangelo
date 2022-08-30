from django.urls import path

from products.views  import ProductIdView, ProductsView


urlpatterns = [
    path("products/", ProductsView.as_view()),
    path("products/<pk>/", ProductIdView.as_view()),
]