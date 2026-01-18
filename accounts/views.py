"""
Представления для регистрации и аутентификации пользователей
"""

from typing import Any

from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer, LoginSerializer, EmptySerializer


class RegisterView(CreateAPIView):
    """
    Представление для регистрации пользователя
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Создание пользователя, создание токена для API, пользователь логинится в сессии
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(
            user=user
        )  # создаём токен для API запросов
        login(request, user)  # логиним пользователя в сессии (для браузера)
        return Response(
            {"username": user.username, "token": token.key},
            status=status.HTTP_201_CREATED,
        )


class LoginView(GenericAPIView):
    """
    Представление для аутентификации пользователя
    """

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Получение токена зарегестрированного пользователя (или создание нового после выхода),
        пользователь логинится в сессии
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        token, _ = Token.objects.get_or_create(
            user=user
        )  # создаём токен для API запросов
        login(request, user)  # логиним пользователя в сессии (для браузера)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    """
    Представление для выхода пользователя
    """

    serializer_class = EmptySerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Удаление токена пользователя, пользователь разлогинивается из сессии
        """

        if hasattr(request.user, "auth_token"):
            print(request.user.auth_token)
            request.user.auth_token.delete()  # удаляем токен
        logout(request)  # разлогиниваем из сессии
        return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
