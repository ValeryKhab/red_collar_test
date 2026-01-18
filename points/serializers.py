"""
Сериализаторы моделей
"""

from rest_framework import serializers
from .models import Point, Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели сообщения

    Fields:
        id: ID сообщения
        text: Текст сообщения
        author: Автор сообщения
        created_at: Дата создания сообщения
        updated_at: Дата последнего изменения сообщения
    """

    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Message
        fields = ("id", "text", "author", "created_at", "updated_at")
        read_only_fields = ["created_at", "updated_at", "author"]


class PointSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели гео-точки

    Fields:
        messages: Сообщения на точке
        name: Название точки
        description: Описание точки
        latitude: Широта
        longitude: Долгота
        creator: Создатель точки
        created_at: Дата создания точки
        updated_at: Дата последнего изменения точки
    """

    creator = serializers.ReadOnlyField(source="creator.username")
    messages = MessageSerializer(many=True, read_only=True, source="message_set")

    class Meta:
        model = Point
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "creator", "messages_count"]
