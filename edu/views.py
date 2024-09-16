from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from edu.models import Course, Lesson
from edu.permissions import IsModerator, IsOwner
from edu.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == "list":
            # Список только для авторизованных
            permission_classes = (IsAuthenticated,)
        elif self.action == "create":
            # Создавать может только авторизованный пользователь, но не для модератор
            permission_classes = (IsAuthenticated & ~IsModerator,)
        elif self.action == "destroy":
            # Удалять может только авторизованный пользователь, являющийся владельцем
            permission_classes = (IsAuthenticated & IsOwner,)
        else:
            # смотреть и редактировать может модератор, либо владелец
            permission_classes = (IsModerator | (IsAuthenticated & IsOwner),)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = self.request.user
        serializer.save()

    def get_queryset(self):
        """
        Полный список курсов виден только модератору.
        Остальным видно только свои курсы.
        """

        if self.action == "list":
            if self.request.user.groups.filter(name="moderators").exists():
                return Course.objects.all()
            return self.queryset.filter(owner=self.request.user)
        return Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Создание урока.
    Может любой зарегистрированный, но не модератор
    """
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated & ~IsModerator,)

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = self.request.user
        serializer.save()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление урока.
    Может только владелец.
    """
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsOwner,)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Просмотр урока.
    Может модератор, либо владелец.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | (IsAuthenticated & IsOwner),)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Редактирование урока.
    Может модератор, либо владелец.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | (IsAuthenticated & IsOwner),)


class LessonListAPIView(generics.ListAPIView):
    """
    Просмотр списка уроков.
    Может модератор, либо владелец своих уроков.
    """
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | (IsAuthenticated & IsOwner),)

    def get_queryset(self):
        if self.request.user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)
