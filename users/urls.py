from django.urls import path
from users.apps import UsersConfig

app_name = UsersConfig.name


from users import views

urlpatterns = [
    path('<int:pk>', views.UserRetrieveAPIView.as_view(), name="retrieve-user"),
    path('create/', views.UserCreateAPIView.as_view(), name="create-user"),
    path('update/<int:pk>/', views.UserUpdateAPIView.as_view(), name="update-user"),

    path('payments/', views.PaymentListAPIView.as_view(), name="payments-list"),
]
