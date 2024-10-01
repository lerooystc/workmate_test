from django.urls import path

from .views import DecoratedTokenObtainPairView
from .views import DecoratedTokenRefreshView
from .views import UserRegister

urlpatterns = [
    path("", DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegister.as_view(), name="register_user"),
]
