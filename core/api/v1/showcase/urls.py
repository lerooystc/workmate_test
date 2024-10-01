from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BreedViewSet
from .views import CatViewSet
from .views import RatingViewSet
from .views import UserRatings


router = DefaultRouter()
router.register("cats", CatViewSet, "cats")
router.register("breeds", BreedViewSet, "breeds")
router.register(r"cats/(?P<cat_id>\d+)/ratings", RatingViewSet, "ratings")

urlpatterns = [
    path("user_ratings/", UserRatings.as_view(), name="user_ratings")
] + router.urls
