from rest_framework import generics

from users.models import User, Payment
from users.serializers import PaymentSerializer, UserSerializer, UserUpdateSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    Редактировать можно любого пользователя кроме админа
    Так же редактирование ограничено полями
    """

    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UserUpdateSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    ordering_fields = ("date",)
    filterset_fields = ["course", "lesson", "method"]
