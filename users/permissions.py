from rest_framework.views import Request
from rest_framework.permissions import BasePermission


class IsAdminPermission(BasePermission):
    def has_permission(self, req: Request, _):
        print(req.user.is_superuser)
        return req.user.is_authenticated and req.user.is_superuser


class IsOwnerAccountPermission(BasePermission):
    def has_permission(self, req: Request, _):
        return req.user.is_authenticated

    def has_object_permission(self, request, _, obj):

        return request.user.is_authenticated and obj == request.user
