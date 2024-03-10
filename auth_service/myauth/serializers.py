import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")

UserModel = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    def create(self, validated_data):
        val1 = json.loads(json.dumps(validated_data.get("_content")))
        val = val1.lstrip("{\r\n ").rstrip(",\r\n}").replace(",", "").replace("\r\n", "").split()
        print(val)
        user = UserModel.objects.create_user(
            username=val[1].strip('"'),
            password=val[3].strip('"'),
            first_name=val[5].strip('"'),
            last_name=val[7].strip('"'),
        )
        return user
    class Meta:
        model = UserModel
        fields = ("id", "username", "password", "first_name", "last_name")