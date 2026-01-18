"""
Сериализаторы моделей
"""

from rest_framework import serializers
from django.contrib.auth.models import User


class EmptySerializer(serializers.Serializer):
    """
    Пустой сериализатор
    """

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели пользователя для регистрации

    Fields:
        username: Имя пользователя
        password: Пароль
    """

    password = serializers.CharField(write_only=True, min_length=6, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор модели пользователя для входа

    Fields:
        username: Имя пользователя
        password: Пароль
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
