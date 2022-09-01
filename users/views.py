from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from .models import Account
from .serializers import AccountSerializer
from .permissions import IsAccountOwner


class AccountView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountOrderView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        num = self.kwargs['num']
        return self.queryset.order_by('-date_joined')[0:num]


class AccountUpdateView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True

        if 'is_active' in request.data:
            request.data.pop('is_active')

        return self.update(request, *args, **kwargs)


class AccountManageView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer




