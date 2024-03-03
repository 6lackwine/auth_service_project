import json

from django.contrib.auth import logout, get_user_model, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializers, UserSerializer


@api_view(["POST"])
def login_view(request):
    if request.method == "POST":
        user_data = json.loads(request.body)
        username = user_data["username"]
        password = user_data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response("Успешно вошли", status=200)
        else:
            raise TypeError("Неверно введен пароль или логин")


@api_view(["GET"])
def logout_view(request):
    logout(request)
    return Response(status=200) #redirect("myauth:login")

# class UpdateAPIView(RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializers

class UserAPIView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if pk == request.user.pk:
            serialized = UserSerializers(user)
            return Response(serialized.data)
        else:
            return Response("Пользователь не авторизирован", status=400)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if pk == request.user.pk:
            user.first_name = request.data["first_name"]
            user.last_name = request.data["last_name"]
            user.save()
            return Response(request.data, status=200)
        else:
            return Response("Пользователя не авторизирован", status=400)

class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class RegisterAPIView(CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer