from rest_framework.routers import DefaultRouter

from .views import BreedViewSet
from .views import CatViewSet


router = DefaultRouter()
router.register("cats", CatViewSet, "cats")
router.register("breeds", BreedViewSet, "breeds")


urlpatterns = [] + router.urls
