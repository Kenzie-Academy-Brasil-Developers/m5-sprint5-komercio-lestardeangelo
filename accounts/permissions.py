from rest_framework.permissions import BasePermission
from rest_framework.views import Request

from accounts.models import Account


class IsAccountOwnerPermission(BasePermission):
    def has_permission(self, request: Request, _):
        return bool(request.user.is_authenticated and request.user)

    def has_object_permission(self, request: Request, _, obj: Account):
        return obj.id == request.user.id
