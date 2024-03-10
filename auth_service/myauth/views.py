from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .serializers import UserSerializers, UserSerializer


class LoginViewClass(APIView):
    def post(self, request):
        if request.method == "POST":
            user_data = request.data
            username = user_data.get("username")
            password = user_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is None:
                return Response("Неверные данные", 401)
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
            login(request, user)
            return Response({
                "refresh": str(refresh),
                "access": str(access)
            }, 200)


class LogoutAPIView(APIView):
    def get(self, request):
        refresh_token = request.data.get('token')
        print(refresh_token, "TOKEN")
        if not refresh_token:
            return Response({'error': 'Необходим Refresh token'}, status=400)
        try:
            token = RefreshToken(refresh_token)
            print(token, "ПРОВЕРКА")
            token.blacklist()
        except Exception as e:
            return Response({'error': 'Неверный Refresh token'}, status=400)
        logout(request)
        return Response({'success': 'Выход успешен'}, status=200)

class UserAPIView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            serialized = UserSerializers(user)
            return Response(serialized.data)
        else:
             return Response("Пользователь не авторизирован", status=401)

    def post(self, request):
        if request.user.is_authenticated:
            request.user.first_name = request.data.get("first_name")
            request.user.last_name = request.data.get("last_name")
            request.user.save()
            return Response(request.data, status=200)
        else:
            return Response("Пользователя не авторизирован", status=401)

class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
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