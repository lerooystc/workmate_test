from apps.showcase.models import Breed
from apps.showcase.models import Cat
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
            "name",
            "age",
            "color",
            "description",
            "breed",
        )
