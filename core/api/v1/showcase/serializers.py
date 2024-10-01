from apps.showcase.models import Breed
from apps.showcase.models import Cat
from apps.showcase.models import Rating
from rest_framework.serializers import CharField
from rest_framework.serializers import ModelSerializer


class BreedSerializer(ModelSerializer):
    class Meta:
        model = Breed
        fields = ("name",)


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
    breed = BreedSerializer()
    color = CharField(source="get_color_display")

    class Meta:
        model = Cat
        fields = (
            "id",
            "name",
            "age",
            "color",
            "description",
            "breed",
        )


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
