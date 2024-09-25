from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from edu.permissions import IsModerator
from users.models import User, Payment
from users.permissions import IsOwnerUserProfile
from users.serializers import (
    PaymentSerializer,
    RegisterSerializer,
    UserOwnerSerializer,
    UserGeneralSerializer,
    UserModeratorSerializer,
)
from users.services import create_product, create_session


class UserCreateAPIView(generics.CreateAPIView):
    """
    Регистрация.
    Только неавторизованный пользователь может зарегистрироваться
    """

    serializer_class = RegisterSerializer
    permission_classes = (~IsAuthenticated,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Просмотр профиля пользователя.
    Для модератора, владельца и всех остальных разные сериализаторы.
    """

    queryset = User.objects.all()

    @swagger_auto_schema(
        responses={200: openapi.Response("response description", UserOwnerSerializer)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):

        if self.request.user == self.get_object():
            return UserOwnerSerializer
        elif self.request.user.groups.filter(name="moderators").exists():
            return UserModeratorSerializer
        return UserGeneralSerializer


class UserListAPIView(generics.ListAPIView):
    """
    Профсмотр списка пользователей.
    Для модератора и всех остальных разные сериализаторы.
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user.groups.filter(name="moderators").exists():
            return UserModeratorSerializer
        return UserGeneralSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    """Редактирование профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserOwnerSerializer
    permission_classes = (IsAuthenticated & IsOwnerUserProfile,)

    def perform_update(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление пользователя.
    Только модератор может удалять.
    """

    queryset = User.objects.all()
    permission_classes = (IsModerator,)


class PaymentListAPIView(generics.ListAPIView):
    """Список платежей."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    ordering_fields = ("date",)
    filterset_fields = ["course", "lesson", "method"]
    permission_classes = (IsModerator,)


class PaymentCreateAPIView(generics.CreateAPIView):
    """Создание платежа. Необходимо указать либо id курса, либо id урока"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_name = payment.course.name if payment.course else payment.lesson.name
        product = create_product(product_name, payment.amount)
        url, session_id = create_session(product)
        payment.session_id = session_id
        payment.link = url
        payment.save()
