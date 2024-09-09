from django.urls import path
from users.apps import UsersConfig

app_name = UsersConfig.name


from users import views

urlpatterns = [
    path('create/', views.UserCreateAPIView.as_view(), name="create-lesson"),
    path('update/<int:pk>/', views.UserUpdateAPIView.as_view(), name="update-lesson"),
]
