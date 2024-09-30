from apps.showcase.models import Breed
from apps.showcase.models import Cat
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


class ReadCatSerializer(ModelSerializer):
    breed = BreedSerializer()

    class Meta:
        model = Cat
        fields = (
            "name",
            "age",
            "color",
            "description",
            "breed",
        )
