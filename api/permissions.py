from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrMe(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated 
                and (request.user.is_superuser 
                     or request.user.role == 'admin'
                     or view.kwargs.get('pk', None) == 'me'))


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in SAFE_METHODS)


class IsAdminOrReadOnly(BasePermission):
    def has_permissions(self, request, view, obj):
        return (request.user.is_superuser
                or request.user.role == 'admin'
                or request.method in SAFE_METHODS)


class IsModeratorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'moderator'
                or request.method in SAFE_METHODS)
