from rest_framework import serializers

from edu.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = ("name", "description", "preview", "count_lessons", "lessons")

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course__id=course.id).count()
