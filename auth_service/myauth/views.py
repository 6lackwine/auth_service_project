import json

import rest_framework_simplejwt.tokens
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout, get_user_model, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .serializers import UserSerializers, UserSerializer



@api_view(["POST"])
def login_view(request):
    if request.method == "POST":
        user_data = request.data
        print(user_data)
        a = json.loads(json.dumps(user_data.get("_content")))
        b = a.lstrip("{\r\n ").rstrip(",\r\n}").replace(",", "").replace("\r\n", "").split()
        print(b)
        username = b[1].strip('"')
        password = b[3].strip('"')
        user = authenticate(request, username=username, password=password)
        print(user, "AAA")
        if user is None:
            # login(request, user)
            # return Response("Успешно вошли", status=200)
        # else:
        #     raise TypeError("Неверно введен пароль или логин")
            return Response("Неверные данные", 401)
        refresh = RefreshToken.for_user(user)
        print(refresh)
        refresh.payload.update({
            "user_id": user.id,
            "username": user.username
        })
        print(refresh.payload, "GGGG")
        access = AccessToken.for_user(user)
        access.payload.update({
            "user_id": user.id,
            "username": user.username
        })
        print(access, "ACCESS")
        print(access.payload, "ACCESS2")
        login(request, user)
        return Response({
            "refresh": str(refresh),
            "access": str(access)
        }, 200)
        # login(request, user)
        # return Response("ok", 200)

class LoginViewClass(APIView):
    #permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.method == "POST":
            user_data = request.data
            print(user_data)
            a = json.loads(json.dumps(user_data.get("_content")))
            b = a.lstrip("{\r\n ").rstrip(",\r\n}").replace(",", "").replace("\r\n", "").split()
            print(b)
            username = b[1].strip('"')
            password = b[3].strip('"')
            user = authenticate(request, username=username, password=password)
            print(user, "AAA")
            if user is None:
                # login(request, user)
                # return Response("Успешно вошли", status=200)
                # else:
                #     raise TypeError("Неверно введен пароль или логин")
                return Response("Неверные данные", 401)
            refresh = RefreshToken.for_user(user)
            print(refresh)
            refresh.payload.update({
                "user_id": user.id,
                "username": user.username
            })
            print(refresh.payload, "GGGG")
            access = AccessToken.for_user(user)
            access.payload.update({
                "user_id": user.id,
                "username": user.username
            })
            print(access, "ACCESS")
            print(access.payload, "ACCESS2")
            login(request, user)
            return Response({
                "refresh": str(refresh),
                "access": str(access)
            }, 200)
            # login(request, user)
            # return Response("ok", 200)


@api_view(["GET"])
def logout_view(request):
    logout(request)
    return Response(status=200) #redirect("myauth:login")


class LogoutAPIView(APIView):
    def get(self, request):
        refresh_token = RefreshToken.for_user(request.user)
        print(request.data, "TOKEN")
        #print(RefreshToken.for_user(request.user))
        if not refresh_token:
            return Response({'error': 'Необходим Refresh token'}, status=400)
        try:
            token = RefreshToken(refresh_token)
            print(token, "ПРОВЕРКА")
            token.blacklist() # Добавить его в чёрный список
        except Exception as e:
            return Response({'error': 'Неверный Refresh token'}, status=400)
        logout(request)
        return Response({'success': 'Выход успешен'}, status=200)

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
            return Response("Пользователь не авторизирован", status=401)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if pk == request.user.pk:
            user.first_name = request.data["first_name"]
            user.last_name = request.data["last_name"]
            user.save()
            return Response(request.data, status=200)
        else:
            return Response("Пользователя не авторизирован", status=401)

class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class RegisterAPIView(APIView):
    # model = get_user_model()
    # serializer_class = UserSerializer

    def post(self, request):
        print(request.data)
        #serializer = UserSerializer.create(request.data, request.data)
        val1 = json.loads(json.dumps(request.data.get("_content")))
        val = val1.lstrip("{\r\n ").rstrip(",\r\n}").replace(",", "").replace("\r\n", "").split()
        print(str(val[1].strip('"')))
        user = User.objects.create_user(
            username=str(val[1].strip('"')),
            password=str(val[3].strip('"')),
            first_name=str(val[5].strip('"')),
            last_name=str(val[7].strip('"')),
        )
        user.save()
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            "user_id": user.id,
            "username": user.username
        })
        access = AccessToken.for_user(user)
        access.payload.update({
            "user_id": user.id,
            "username": user.username
        })
        return Response({
            "refresh": str(refresh),
            "access": str(access)
        }, status=201)