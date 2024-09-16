from rest_framework import serializers

from edu.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор на уроки."""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор на курсы.
    Дополнительное поле: количество уроков, относящихся к курсу.
    """

    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False)

    class Meta:
        model = Course
        fields = ("name", "description", "preview", "count_lessons", "lessons", "owner")

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course__id=course.id).count()
