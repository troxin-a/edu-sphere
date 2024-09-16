from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверка на модератора."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    """Проверка на владение объектом."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
