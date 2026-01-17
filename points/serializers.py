"""
Сериализаторы моделей
"""

from rest_framework import serializers
from .models import Point, Message


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Message
        fields = ("id", "text", "author", "created_at", "updated_at")
        read_only_fields = ["created_at", "updated_at", "author"]


class PointSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")
    messages_сount = MessageSerializer(many=True, read_only=True, source="message_set")
    
    class Meta:
        model = Point
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "creator", "messages_count"]
