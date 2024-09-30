from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @extend_schema(tags=["Токен"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @extend_schema(tags=["Токен"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
