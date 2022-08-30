from django.urls import path

from users.views import (
    UserView,
    UserDetailView,
    UserLoginView,
    UserViewID,
    UserViewByDateJoined,
    UserAdminManageAccountView,
)


urlpatterns = [
    path("accounts/", UserView.as_view()),  # ACESSO LIVRE
    path("accounts/id/", UserViewID.as_view()),  # ACESSO SOMENTE ADM/SUPERUSER
    path(
        "accounts/<uuid:pk>/", UserDetailView.as_view()
    ),  # MODIFICAR VIEW - # ACESSO SOMENTE DONO DA CONTA
    path(
        "accounts/<uuid:pk>/management/", UserAdminManageAccountView.as_view()
    ),  # ACESSO SOMENTE ADM/SUPERUSER
    path("accounts/newest/<int:num>/", UserViewByDateJoined.as_view()),  # ACESSO LIVRE
    path("login/", UserLoginView.as_view()),  # ACESSO LIVRE
]
