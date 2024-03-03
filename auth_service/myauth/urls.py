from django.urls import path

from .views import logout_view, UserListAPIView, RegisterAPIView, UserAPIView, login_view

app_name = "myauth"

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("sign-up/", RegisterAPIView.as_view(), name="register"),
    path("user/<int:pk>/", UserAPIView.as_view(), name="about-me"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]