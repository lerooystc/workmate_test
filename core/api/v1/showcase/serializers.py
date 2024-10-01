from apps.showcase.models import Breed
from apps.showcase.models import Cat
from apps.showcase.models import Rating
from django.db.models import Avg
from rest_framework.serializers import CharField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField


class BreedSerializer(ModelSerializer):
    class Meta:
        model = Breed
        fields = (
            "id",
            "name",
        )


class CatSerializer(ModelSerializer):
    class Meta:
        model = Cat
        fields = (
            "name",
            "age",
            "color",
            "description",
            "breed",
        )

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class ReadCatSerializer(ModelSerializer):
    breed = CharField(source="breed.name")
    color = CharField(source="get_color_display")
    avg_rating = SerializerMethodField()

    class Meta:
        model = Cat
        fields = (
            "id",
            "name",
            "age",
            "color",
            "description",
            "breed",
            "avg_rating",
        )

    def get_avg_rating(self, obj) -> float | None:
        ratings = obj.ratings.all()
        if ratings.count() > 0:
            return ratings.aggregate(avg=Avg("rating"))["avg"]
        return None


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ("rating",)


class ReadRatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            "user",
            "cat",
            "rating",
        )
