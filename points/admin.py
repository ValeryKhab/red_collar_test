"""
Добавление в admin
"""

from django.contrib import admin
from .models import Point, Message


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    """
    Admin-представление для модели гео-точки
    """

    list_display = (
        "id",
        "name",
        "description",
        "creator",
        "latitude",
        "longitude",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "creator",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "description",
    )


@admin.register(Message)
class MessageUserAdmin(admin.ModelAdmin):
    """
    Admin-представление для модели сообщения
    """

    list_display = (
        "id",
        "text",
        "author",
        "point",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "author",
        "point",
        "created_at",
        "updated_at",
    )
