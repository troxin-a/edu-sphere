from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from edu.models import Course, Lesson, Subscription
from edu.paginators import ResultsSetPagination
from edu.permissions import IsModerator, IsOwner
from edu.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from edu.service import update_course
from edu.tasks import send_email_about_course_update


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = ResultsSetPagination

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            # Список и просмотр курса только для авторизованных
            permission_classes = (IsAuthenticated,)
        elif self.action == "create":
            # Создавать может только авторизованный пользователь, но не для модератор
            permission_classes = (IsAuthenticated & ~IsModerator,)
        elif self.action == "destroy":
            # Удалять может только авторизованный пользователь, являющийся владельцем
            permission_classes = (IsAuthenticated & IsOwner,)
        else:
            # редактировать может модератор, либо владелец
            permission_classes = (IsModerator | (IsAuthenticated & IsOwner),)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = self.request.user
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
        instance = self.get_object()
        update_course(instance.id)

    # def get_queryset(self):
    #     """
    #     Полный список курсов виден только модератору.
    #     Остальным видно только свои курсы.
    #     """

    #     if self.action == "list":
    #         if self.request.user.groups.filter(name="moderators").exists():
    #             return Course.objects.all()
    #         return self.queryset.filter(owner=self.request.user)
    #     return Course.objects.all()


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

        course = serializer.instance.course
        update_course(course.id)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление урока.
    Может только владелец.
    """

    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated & IsOwner,)

    def perform_destroy(self, instance):
        course = Course.objects.get(pk=instance.course.id)
        update_course(course.id)

        instance.delete()


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

    def perform_update(self, serializer):
        """Если у урока меняется курс, отправить уведомления на оба курса: старый и новый"""

        lesson = self.get_object()
        course = Course.objects.get(pk=lesson.course.id)
        update_course(course.id)

        serializer.save()

        new_course = serializer.instance.course
        if course != new_course:
            update_course(new_course.id)


class LessonListAPIView(generics.ListAPIView):
    """
    Просмотр списка уроков.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | (IsAuthenticated & IsOwner),)
    pagination_class = ResultsSetPagination

    # def get_queryset(self):
    #     if self.request.user.groups.filter(name="moderators").exists():
    #         return Lesson.objects.all()
    #     return Lesson.objects.filter(owner=self.request.user)


class SubscriptionAPIView(views.APIView):
    """
    Создание/удаление подписки.
    """

    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=SubscriptionSerializer,
        operation_description="Создание/удаление подписки.",
        responses={201: "'message': 'Подписка создана/удалена'"},
    )
    def post(self, *args, **kwargs):

        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
        return Response({"message": message})
