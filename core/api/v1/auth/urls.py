from django.urls import path

from .views import DecoratedTokenObtainPairView
from .views import DecoratedTokenRefreshView

urlpatterns = [
    path("", DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
]
