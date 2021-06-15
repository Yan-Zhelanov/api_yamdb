from rest_framework.permissions import BasePermission


class IsAdminOrMe(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'admin' or view.kwargs.get('pk', None) == 'me')