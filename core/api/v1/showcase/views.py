from apps.common.perms import IsOwner
from apps.showcase.models import Breed
from apps.showcase.models import Cat
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .serializers import BreedSerializer
from .serializers import CatSerializer
from .serializers import ReadCatSerializer


class BreedViewSet(ListModelMixin, GenericViewSet):
    queryset = Breed.objects.order_by("name")
    serializer_class = BreedSerializer

    @extend_schema(tags=["Порода"])
    def list(self, request, *args, **kwargs):
        """Получить список пород."""
        return super().list(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(tags=["Кот"]),
    retrieve=extend_schema(tags=["Кот"]),
    create=extend_schema(tags=["Кот"]),
    update=extend_schema(tags=["Кот"]),
    partial_update=extend_schema(tags=["Кот"]),
    destroy=extend_schema(tags=["Кот"]),
)
class CatViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Cat.objects.select_related("breed").order_by("name")
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
        elif self.action == "create":
            return [IsAuthenticated()]
        return super().get_permissions()
