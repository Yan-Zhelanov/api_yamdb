from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrMe(BasePermission):
    def has_permission(self, request, view):
        return (view.kwargs.get('pk', None) == 'me'
                or request.user.is_superuser 
                or request.user.role == 'admin')


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)


class IsModeratorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.role == 'moderator')


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_superuser
                         or request.user.role == 'admin')))
