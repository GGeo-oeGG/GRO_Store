from rest_framework.permissions import BasePermission


class OwnerOnlyPerm(BasePermission):
    """Разрешения на обновление."""

    def has_object_permission(self, request, view, obj):
        return obj == request.user
