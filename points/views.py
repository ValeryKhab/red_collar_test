"""
Представления
"""

from math import radians, cos, sin, asin, sqrt
from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import CreateAPIView, GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import RegisterSerializer, LoginSerializer, EmptySerializer, PointSerializer, MessageSerializer
from .models import Point, Message
from .permissions import IsOwner


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)  # создаём токен для API запросов
        login(request, user)  # логиним пользователя в сессии (для браузера)
        return Response(
            {"username": user.username, "token": token.key},
            status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)  # создаём токен для API запросов
        login(request, user)  # логиним пользователя в сессии (для браузера)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    serializer_class = EmptySerializer

    def post(self, request, *args, **kwargs):
        if hasattr(request.user, "auth_token"):
            request.user.auth_token.delete()  # удаляем токен
        logout(request)  # разлогиниваем из сессии
        return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)


class PointListCreateView(ListCreateAPIView):
    serializer_class = PointSerializer
    queryset = Point.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class MessageListCreateView(ListCreateAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        return Message.objects.filter(point_id=self.kwargs["point_id"])

    def perform_create(self, serializer):
        point = Point.objects.get(id=self.kwargs["point_id"])
        serializer.save(author=self.request.user, point=point)


class PointRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = PointSerializer
    permission_classes = [IsOwner, IsAuthenticated]
    queryset = Point.objects.all()
    lookup_field = "id"
    
    
class MessageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsOwner, IsAuthenticated]
    queryset = Message.objects.all()
    lookup_field = "id"


class PointSearchView(GenericAPIView):
    serializer_class = PointSerializer
    queryset = Point.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            lat = float(request.query_params["latitude"])
            lon = float(request.query_params["longitude"])
            radius_km = float(request.query_params["radius"])
        except (KeyError, ValueError):
            return Response(
                {"detail": "latitude, longitude and radius are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        def haversine(lat1, lon1, lat2, lon2):
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            return 6371 * (2 * asin(sqrt(a)))

        points_in_radius = []
        for point in Point.objects.prefetch_related("message_set"):
            if haversine(lat, lon, point.latitude, point.longitude) <= radius_km:
                points_in_radius.append(point)

        serializer = self.get_serializer(points_in_radius, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
