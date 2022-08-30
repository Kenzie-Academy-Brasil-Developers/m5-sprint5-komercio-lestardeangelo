from rest_framework.views import Request
from rest_framework.permissions import BasePermission


class IsAuthenticatedSellerPermission(BasePermission):
    def has_permission(self, request: Request, _):

        if request.method == "POST":

            return request.user.is_authenticated and request.user.is_seller

        return True


class IsAuthenticatedOwnerSellerPermission(BasePermission):
    def has_permission(self, request: Request, _):
        if request.method == "PATCH":

            return request.user.is_authenticated and request.user.is_seller

        return True

    def has_object_permission(self, request: Request, _, obj):
        if request.method == "PATCH":

            return request.user.is_authenticated and obj.user == request.user

        return True
