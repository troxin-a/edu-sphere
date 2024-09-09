from rest_framework import generics

from users.models import User
from users.serializers import UserSerializer, UserUpdateSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    '''
    Редактировать можно любого пользователя кроме админа
    Так же редактирование ограничено полями
    '''
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UserUpdateSerializer
