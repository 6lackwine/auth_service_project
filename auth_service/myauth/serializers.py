from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")

UserModel = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user
    class Meta:
        model = UserModel
        fields = ("id", "username", "password", "first_name", "last_name")