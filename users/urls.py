from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import AllowAny
from django.urls import path

from users.apps import UsersConfig
from users import views

app_name = UsersConfig.name


urlpatterns = [
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("", views.UserListAPIView.as_view(), name="list-user"),
    path("<int:pk>", views.UserRetrieveAPIView.as_view(), name="detail-user"),
    path("register/", views.UserCreateAPIView.as_view(), name="create-user"),
    path("update/<int:pk>/", views.UserUpdateAPIView.as_view(), name="update-user"),
    path("delete/<int:pk>/", views.UserDestroyAPIView.as_view(), name="destroy-user"),
    path("payments/", views.PaymentListAPIView.as_view(), name="payments-list"),
]
