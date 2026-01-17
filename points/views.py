"""
Представления
"""

from math import radians, cos, sin, asin, sqrt
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import PointSerializer, MessageSerializer
from .models import Point, Message
from .permissions import IsOwner


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
