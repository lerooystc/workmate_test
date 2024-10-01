from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import UserRegistrationSerializer


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        tags=["Аутентификация"],
        responses={
            200: OpenApiResponse(
                response=TokenObtainPairSerializer,
                description="Получены валидные данные для входа. Возвращены access и refresh токены.",
            ),
            401: OpenApiResponse(
                description="Получен инвалидные данные. Возвращена ошибка."
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """Получает на вход username и password, возвращает refresh и access токены JWT."""
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @extend_schema(
        tags=["Аутентификация"],
        responses={
            200: OpenApiResponse(
                response=TokenRefreshSerializer,
                description="Получен валидный токен. Возвращен access токен.",
            ),
            401: OpenApiResponse(
                description="Получен инвалидный токен. Возвращена ошибка."
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """Получает на вход refresh токен, возвращает access токен JWT если refresh валиден, иначе 401."""
        return super().post(request, *args, **kwargs)


class UserRegister(APIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = UserRegistrationSerializer

    @extend_schema(
        tags=["Аутентификация"],
        responses={
            201: OpenApiResponse(
                response=UserRegistrationSerializer, description="Создан пользователь."
            ),
            400: OpenApiResponse(description="Не удалось создать пользователя."),
        },
    )
    def post(self, request):
        """Создает нового пользователя с входными данными email, username, password."""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"Bad Request": "Invalid data..."}, status=status.HTTP_400_BAD_REQUEST
            )
