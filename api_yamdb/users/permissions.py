from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_superuser


class IsAdminOrSuperUserList(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_superuser


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class SafeMethods(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.is_moderator


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.is_admin or request.user.is_superuser
