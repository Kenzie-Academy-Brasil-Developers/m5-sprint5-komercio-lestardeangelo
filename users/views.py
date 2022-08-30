from django.contrib.auth import authenticate
from rest_framework import authentication, generics
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Request, Response, status

from .models import User
from .permissions import IsAdminPermission, IsOwnerAccountPermission
from .serializers import (
    LoginSerializer,
    UserSerializer,
    UserSerializerID,
    UserManageAdminSerializer,
)


class UserViewID(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializerID

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminPermission]


class UserView(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwnerAccountPermission]


class UserAdminManageAccountView(generics.UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserManageAdminSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminPermission]


class UserViewByDateJoined(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):

        max_users = self.kwargs["num"]

        return self.queryset.order_by("-date_joined")[0:max_users]


class UserLoginView(APIView):
    def post(self, req: Request):

        serialized = LoginSerializer(data=req.data)
        serialized.is_valid(raise_exception=True)

        user: User = authenticate(**serialized.validated_data)

        if not user:
            return Response(
                {"detail": "Invalid email or password."}, status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status.HTTP_200_OK)
