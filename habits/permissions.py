from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    """Проверка пользователь=владелец привычки"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
