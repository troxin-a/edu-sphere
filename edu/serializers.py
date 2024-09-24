from rest_framework import serializers

from edu.models import Course, Lesson, Subscription
from edu.validators import YoutubeOnly


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор на уроки."""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = (
            YoutubeOnly(
                fields=(
                    "name",
                    "description",
                    "video_url",
                )
            ),
        )


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор на курсы.
    Дополнительное поле: количество уроков, относящихся к курсу.
    Дополнительное поле: флаг подписки пользователя на текущий курс
    """

    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("name", "is_subscribed", "description", "preview", "count_lessons", "lessons", "owner")
        validators = (
            YoutubeOnly(
                fields=(
                    "name",
                    "description",
                )
            ),
        )

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        user = self.context["request"].user
        if Subscription.objects.filter(course=course, user=user).exists():
            return "Вы подписаны"
        else:
            return "Вы не подписаны"


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор на подписки."""

    class Meta:
        model = Subscription
        fields = "__all__"
