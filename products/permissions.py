from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.views import Request


class IsSeller(BasePermission):
    def has_permission(self, request: Request, _):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user and request.user.is_authenticated and request.user.is_seller
        )
