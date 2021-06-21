from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.roles import USER, MODERATOR, ADMIN


class IsAdminOrMe(BasePermission):
    def has_permission(self, request, view):
        return (
            view.kwargs.get('pk') == 'me'
            or request.user.role == ADMIN
            or request.user.is_staff
            or request.user.is_superuser
        )


class IsAuthorOrModeratorOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.role == MODERATOR
            or request.user.role == ADMIN
            or request.user.is_staff
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
                and (request.user.role == ADMIN
                     or request.user.is_staff
                     or request.user.is_superuser))
        )
