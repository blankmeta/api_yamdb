from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_superuser


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class AdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_superuser


class AdminOrSuperuserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin or request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(
                request.user.is_admin or request.user.is_superuser)


class IsStaffOrAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (obj.author == request.user or request.user.role in (
                'admin', 'moderator') or request.user.is_superuser)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
