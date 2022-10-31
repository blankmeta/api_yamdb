from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or request.user.is_superuser


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class AdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser
