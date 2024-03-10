from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from .views import logout_view, UserListAPIView, RegisterAPIView, UserAPIView, \
    login_view, LoginViewClass, LogoutAPIView

app_name = "myauth"

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("sign-up/", RegisterAPIView.as_view(), name="register"),
    path("user/<int:pk>/", UserAPIView.as_view(), name="about-me"),
    path("login/", LoginViewClass.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    #path('logout/', TokenBlacklistView.as_view(), name='token_blacklist')
]