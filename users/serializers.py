from rest_framework import serializers
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class ClassModerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "id")
