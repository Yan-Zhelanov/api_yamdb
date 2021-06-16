from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permissions(self, request, view, obj):
        return (request.user.is_staff
                or request.method in permissions.SAFE_METHODS)


class IsModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'moderator'
                or request.method in permissions.SAFE_METHODS)
