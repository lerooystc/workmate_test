from apps.common.perms import IsOwner
from apps.showcase.models import Breed
from apps.showcase.models import Cat
from apps.showcase.models import Rating
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from drf_spectacular.utils import OpenApiResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import BreedSerializer
from .serializers import CatSerializer
from .serializers import RatingSerializer
from .serializers import ReadCatSerializer
from .serializers import ReadRatingSerializer


@extend_schema_view(
    create=extend_schema(
        tags=["Порода"],
        responses={
            201: OpenApiResponse(
                response=BreedSerializer, description="Создана порода."
            ),
            400: OpenApiResponse(
                description="Не удалось создать породу. Инвалидные данные."
            ),
            401: OpenApiResponse(description="Нет прав доступа на создание породы."),
        },
    ),
    update=extend_schema(
        tags=["Порода"],
        responses={
            200: OpenApiResponse(
                response=BreedSerializer, description="Изменены данные о породе."
            ),
            400: OpenApiResponse(
                description="Не удалось создать породу. Инвалидные данные."
            ),
            401: OpenApiResponse(description="Нет прав доступа на изменение породы."),
            404: OpenApiResponse(description="Порода не найдена."),
        },
    ),
    destroy=extend_schema(
        tags=["Порода"],
        responses={
            204: OpenApiResponse(description="Удалены данные о породы."),
            401: OpenApiResponse(description="Нет прав доступа на удаление породы."),
            404: OpenApiResponse(description="Порода не найдена."),
        },
    ),
)
class BreedViewSet(
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Breed.objects.order_by("id")
    serializer_class = BreedSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["get", "post", "put", "delete"]

    def get_permissions(self):
        if self.action in ("destroy", "update", "create"):
            return [IsAdminUser()]
        return super().get_permissions()

    @extend_schema(tags=["Порода"])
    def list(self, request, *args, **kwargs):
        """Получить список пород."""
        return super().list(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        tags=["Кот"],
        responses={
            200: OpenApiResponse(response=CatSerializer, description="Список котов."),
            400: OpenApiResponse(
                description="Инвалидные данные (порода). Не удалось получить котов."
            ),
        },
    ),
    retrieve=extend_schema(
        tags=["Кот"],
        responses={
            200: OpenApiResponse(
                response=ReadCatSerializer, description="Получены данные о коте."
            ),
            404: OpenApiResponse(description="Кот не найден."),
        },
    ),
    create=extend_schema(
        tags=["Кот"],
        responses={
            201: OpenApiResponse(response=CatSerializer, description="Создан кот."),
            400: OpenApiResponse(
                description="Не удалось создать кота. Инвалидные данные."
            ),
        },
    ),
    update=extend_schema(
        tags=["Кот"],
        responses={
            200: OpenApiResponse(
                response=CatSerializer, description="Изменены данные о коте."
            ),
            400: OpenApiResponse(
                description="Не удалось создать кота. Инвалидные данные."
            ),
            403: OpenApiResponse(description="Нет прав доступа на изменение кота."),
            404: OpenApiResponse(description="Кот не найден."),
        },
    ),
    partial_update=extend_schema(
        tags=["Кот"],
        responses={
            200: OpenApiResponse(
                response=CatSerializer, description="Изменены данные о коте."
            ),
            400: OpenApiResponse(
                description="Не удалось создать кота. Инвалидные данные."
            ),
            403: OpenApiResponse(description="Нет прав доступа на изменение кота."),
            404: OpenApiResponse(description="Кот не найден."),
        },
    ),
    destroy=extend_schema(
        tags=["Кот"],
        responses={
            204: OpenApiResponse(description="Удалены данные о коте."),
            403: OpenApiResponse(description="Нет прав доступа на удаление кота."),
            404: OpenApiResponse(description="Кот не найден."),
        },
    ),
)
class CatViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Cat.objects.select_related("breed").order_by("-id")
    serializer_class = CatSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("breed",)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadCatSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ("destroy", "update", "partial_update"):
            return [IsOwner()]
        elif self.action in ("create",):
            return [IsAuthenticated()]
        return super().get_permissions()

    def create(self, request):
        serializer = CatSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            instance = serializer.save()
            response_object = ReadCatSerializer(instance)
            return Response(response_object.data, status=status.HTTP_201_CREATED)
        return Response(
            {"Bad Request": "Invalid data..."}, status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema_view(
    list=extend_schema(
        tags=["Оценка"],
        responses={
            200: OpenApiResponse(response=CatSerializer, description="Список оценок."),
            404: OpenApiResponse(description="Кот не найден."),
        },
    ),
    create=extend_schema(
        tags=["Оценка"],
        request=RatingSerializer,
        responses={
            201: OpenApiResponse(response=RatingSerializer, description="Кот оценен."),
            400: OpenApiResponse(
                description="Не удалось оценить кота. Инвалидные данные."
            ),
            401: OpenApiResponse(description="Нет доступа."),
            404: OpenApiResponse(description="Кот не найден."),
        },
    ),
)
class RatingViewSet(
    ListModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = Rating.objects.select_related("cat", "user")
    serializer_class = ReadRatingSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        if self.action == "list":
            cat = get_object_or_404(Cat, id=self.kwargs["cat_id"])
            return Rating.objects.filter(cat=cat)
        return super().get_queryset()

    def get_object(self):
        """Получает оценку пользователя по коту."""
        cat = get_object_or_404(Cat, id=self.kwargs["cat_id"])
        return get_object_or_404(Rating, user=self.request.user, cat=cat)

    def get_permissions(self):
        if self.action in (
            "create",
            "rate_a_cat",
            "get_cat_rating",
            "update_cat_rating",
        ):
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        """
        Получает оценки кота.

        В случае несуществующей оценки/кота - 404.

        :param cat_id: ID кота.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=["Оценка"],
        responses={
            200: OpenApiResponse(
                response=ReadRatingSerializer, description="Оценка кота."
            ),
            401: OpenApiResponse(description="Нет доступа."),
            404: OpenApiResponse(description="Кот или оценка не найдена."),
        },
    )
    @action(methods=["GET"], detail=False, url_path="get_user_rating")
    def get_cat_rating(self, request, cat_id):
        """
        Получение пользовательской оценки кота.

        Получает оценку в случае авторизованного пользователя, иначе 401.
        В случае несуществующей оценки/кота - 404.

        :param cat_id: ID кота.
        """
        rating = self.get_object()
        serializer = ReadRatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, cat_id):
        """
        Добавление оценки кота.

        Добавляет оценку в случае авторизованного пользователя, иначе 401.
        В случае несуществующего кота - 404.
        В случае оценки вне диапазона 0-5 - 400.

        :param cat_id: ID кота.
        """
        cat = get_object_or_404(Cat, id=self.kwargs["cat_id"])
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(user=request.user, cat=cat)
            response_object = ReadRatingSerializer(instance)
            return Response(response_object.data, status=status.HTTP_201_CREATED)
        return Response(
            {"Bad Request": "Invalid data..."}, status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        tags=["Оценка"],
        request=RatingSerializer,
        responses={
            201: OpenApiResponse(response=RatingSerializer, description="Кот изменен."),
            400: OpenApiResponse(
                description="Не удалось изменить оценку кота. Инвалидные данные."
            ),
            401: OpenApiResponse(description="Нет доступа."),
            404: OpenApiResponse(description="Кот не найден."),
        },
    )
    @action(methods=["PATCH"], detail=False, url_path="update_user_rating")
    def update_cat_rating(self, request, cat_id):
        """
        Обновление оценки кота.

        Изменяет оценку авторизованного пользователя, иначе 401.
        В случае несуществующего кота - 404.
        В случае оценки вне диапазона 0-5 - 400.

        :param cat_id: ID кота.
        """
        rating = self.get_object()
        serializer = RatingSerializer(data=request.data, instance=rating)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"Bad Request": "Invalid data..."}, status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema_view(
    get=extend_schema(
        tags=["Оценка"],
        responses={
            200: OpenApiResponse(response=CatSerializer, description="Список оценок."),
            400: OpenApiResponse(
                description="Инвалидные данные. Не удалось получить оценки."
            ),
        },
    ),
)
class UserRatings(ListAPIView):
    """
    Отдельный ListAPIView для получения всех оценок определенного пользователя.
    """

    queryset = Rating.objects.select_related("cat", "user")
    serializer_class = ReadRatingSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("user",)
