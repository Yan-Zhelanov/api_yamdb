from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrMe(BasePermission):
    def has_permission(self, request, view):
        return (
            view.kwargs.get('pk', None) == 'me'
            or request.user.is_superuser
            or request.user.role == 'admin'
        )


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )


class IsAuthorOrModeratorOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
                and (request.user.is_superuser
                    or request.user.role == 'admin'
        )))
