from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView, Request, Response, status

from accounts.models import Account
from accounts.permissions import IsAccountOwnerPermission
from accounts.serializers import (
    AccountIsActiveSerializer,
    AccountSerializer,
    LoginSerializer,
    UpdateAccountIdSerializer,
)


class AccountView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class LoginView(APIView):
    def post(self, request: Request):
        serialized = LoginSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        account: Account = authenticate(**serialized.validated_data)

        if not account:
            return Response(
                {"detail": "Invalid email or password."},
                status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=account)

        return Response({"token": token.key}, status.HTTP_200_OK)


class ActiveDeactiveAccountView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountIsActiveSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]


class UpdateAccountView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = UpdateAccountIdSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAccountOwnerPermission]

    # def partial_update(self, request, *args, **kwargs):
    #     print("\n\n\n", args, "\n\n\n")
    #     print("\n\n\n", kwargs, "\n\n\n")
    #     return super().partial_update(request, *args, **kwargs)
