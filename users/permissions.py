from rest_framework.permissions import BasePermission


class IsOwnerUserProfile(BasePermission):
    """Проверяет на владельца профиля"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user
