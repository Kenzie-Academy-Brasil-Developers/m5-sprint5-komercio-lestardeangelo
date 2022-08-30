from django.urls import path


from products.views import ProductView, ProductIdView

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/<pk>/", ProductIdView.as_view()),
]
