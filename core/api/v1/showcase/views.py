from apps.showcase.models import Breed
from apps.showcase.models import Cat
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import BreedSerializer
from .serializers import CatSerializer
from .serializers import ReadCatSerializer


class BreedViewSet(ListModelMixin, GenericViewSet):
    queryset = Breed.objects.order_by("name")
    serializer_class = BreedSerializer

    def list(self, request, *args, **kwargs):
        """Получить список пород."""
        return super().list(request, *args, **kwargs)


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

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadCatSerializer
        return super().get_serializer_class()
