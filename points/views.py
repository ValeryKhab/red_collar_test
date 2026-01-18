"""
Представления
"""

from math import radians, cos, sin, asin, sqrt
from typing import Any

from django.db.models import QuerySet
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import PointSerializer, MessageSerializer
from .models import Point, Message
from .permissions import IsOwnerOrReadOnly


AVERAGE_EARTH_RADIUS: int = 6371  # средний радиус Земли в километрах


class PointListCreateView(ListCreateAPIView):
    """
    Представление для создания точки и просмотра существующих
    """

    serializer_class = PointSerializer
    queryset = Point.objects.all()

    def perform_create(self, serializer: PointSerializer) -> None:
        """
        Создане новой гео-точки и привязка к текущему пользователю

        Args:
            serializer: Сериализатор гео-точки
        """
        serializer.save(creator=self.request.user)


class MessageListCreateView(ListCreateAPIView):
    """Создание сообщений и получение сообщений для конкретной точки"""

    serializer_class = MessageSerializer

    def get_queryset(self) -> QuerySet[Message]:
        """
        Возвращает список сообщений, относящихся к заданной точке

        Returns:
            QuerySet сообщений
        """

        return Message.objects.filter(point_id=self.kwargs["point_id"])

    def perform_create(self, serializer: MessageSerializer) -> None:
        """
        Создаёт сообщение для указанной гео-точки

        Args:
            serializer: Сериализатор сообщения
        """
        point = Point.objects.get(id=self.kwargs["point_id"])
        serializer.save(author=self.request.user, point=point)


class PointRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление и удаление гео-точки
    """

    serializer_class = PointSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    queryset = Point.objects.all()
    lookup_field = "id"


class MessageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление и удаление сообщения
    """

    serializer_class = MessageSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    queryset = Message.objects.all()
    lookup_field = "id"


class PointSearchView(GenericAPIView):
    """
    Поиск гео-точек и сообщений в заданном радиусе от координат
    """

    serializer_class = PointSerializer
    queryset = Point.objects.all()

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Возвращает гео-точки, находящиеся в пределах заданного радиуса

        Query-параметры:
            latitude: Широта точки поиска
            longitude: Долгота точки поиска
            radius: Радиус поиска в километрах
        """

        try:
            lat = float(request.query_params["latitude"])
            lon = float(request.query_params["longitude"])
            radius_km = float(request.query_params["radius"])
        except (KeyError, ValueError):
            return Response(
                {"detail": "latitude, longitude and radius are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
            """
            Вычисляет расстояние между двумя гео-точками по формуле гаверсинусов

            Args:
                lat1: Широта первой точки
                lon1: Долгота первой точки
                lat2: Широта второй точки
                lon2: Долгота второй точки

            Returns:
                Расстояние между точками в километрах
            """

            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            return AVERAGE_EARTH_RADIUS * (2 * asin(sqrt(a)))

        points_in_radius = []
        for point in Point.objects.prefetch_related("message_set"):
            if haversine(lat, lon, point.latitude, point.longitude) <= radius_km:
                points_in_radius.append(point)

        serializer = self.get_serializer(points_in_radius, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
