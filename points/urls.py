"""
URL-шаблоны
"""

from django.urls import path
from .views import (
    PointListCreateView,
    MessageListCreateView,
    PointRetrieveUpdateDestroyView,
    MessageRetrieveUpdateDestroyView,
    PointSearchView,
)

urlpatterns = [
    path("", PointListCreateView.as_view()),
    path("<int:point_id>/messages/", MessageListCreateView.as_view()),
    path("<int:id>/", PointRetrieveUpdateDestroyView.as_view()),
    path("messages/<int:id>/", MessageRetrieveUpdateDestroyView.as_view()),
    path("search/", PointSearchView.as_view()),
]
