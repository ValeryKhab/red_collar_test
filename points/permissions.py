"""
Уровни доступа
"""

from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Разрешает доступ только владельцу объекта
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "creator"):
            return obj.creator == request.user
        if hasattr(obj, "author"):
            return obj.author == request.user
        return False
