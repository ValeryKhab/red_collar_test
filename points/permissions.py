"""
Уровни доступа
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает безопасные методы (GET, HEAD, OPTIONS) всем,
    а модифицирующие методы (POST, PATCH, DELETE) только владельцу.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if hasattr(obj, "creator"):
            return obj.creator == request.user
        if hasattr(obj, "author"):
            return obj.author == request.user
        return False
