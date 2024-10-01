from django.contrib.auth.models import User
from rest_framework.serializers import CharField
from rest_framework.serializers import ModelSerializer


class UserRegistrationSerializer(ModelSerializer):
    username = CharField(max_length=30)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
        )

    def create(self, validated_data):
        user_obj = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        user_obj.save()
        return user_obj
