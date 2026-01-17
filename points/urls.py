"""
URL-шаблоны
"""

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (RegisterView, LoginView, LogoutView, 
                    PointListCreateView, MessageListCreateView, PointRetrieveUpdateDestroyView, 
                    MessageRetrieveUpdateDestroyView, PointSearchView)

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("", PointListCreateView.as_view()),
    path("<int:point_id>/messages/", MessageListCreateView.as_view()),
    path("<int:id>/", PointRetrieveUpdateDestroyView.as_view()),
    path("messages/<int:id>/", MessageRetrieveUpdateDestroyView.as_view()),
    path("search/", PointSearchView.as_view()),
]
