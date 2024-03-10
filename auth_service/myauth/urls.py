from django.urls import path

from .views import UserListAPIView, RegisterAPIView, UserAPIView, \
     LoginViewClass, LogoutAPIView

app_name = "myauth"

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("sign-up/", RegisterAPIView.as_view(), name="register"),
    path("user/me/", UserAPIView.as_view(), name="about-me"),
    path("login/", LoginViewClass.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]