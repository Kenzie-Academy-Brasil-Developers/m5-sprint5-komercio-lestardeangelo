from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from . import views

urlpatterns = [
   path('accounts/', views.AccountView.as_view(), name="account-register"),
   path('accounts/newest/<int:num>/', views.AccountOrderView.as_view(), name="list-view"),
   path('login/', ObtainAuthToken.as_view(), name="login"),
   path('accounts/<pk>/', views.AccountUpdateView.as_view(), name="account-update"),
   path('accounts/<pk>/management/', views.AccountManageView.as_view(), name="account-manager")
]