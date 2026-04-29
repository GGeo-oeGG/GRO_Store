from rest_framework.permissions import BasePermission


class OwnerOnlyPerm(BasePermission):
    """Разрешения на обновление."""

    def has_permission(self, request, view):
        obj = view.get_object()
        return request.user == obj.owner
