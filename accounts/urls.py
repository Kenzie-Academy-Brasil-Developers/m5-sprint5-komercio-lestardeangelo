from django.urls import path

from accounts.views import (
    AccountView,
    LoginView,
    ActiveDeactiveAccountView,
    UpdateAccountView,
)


urlpatterns = [
    path("accounts/", AccountView.as_view()),
    path("accounts/<pk>/management/", ActiveDeactiveAccountView.as_view()),
    path("accounts/<pk>/", UpdateAccountView.as_view()),
    path("login/", LoginView.as_view()),
]
