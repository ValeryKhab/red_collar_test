"""
Сериализаторы моделей
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Point, Message


class EmptySerializer(serializers.Serializer):
    pass


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("username", "password", "email")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


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
