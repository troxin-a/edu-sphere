from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}

class Course(models.Model):
    name = models.CharField(verbose_name="Название", max_length=150)
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    preview = models.ImageField(verbose_name="Превью", upload_to="courses", **NULLABLE)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(verbose_name="Название", max_length=150)
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    preview = models.ImageField(verbose_name="Превью", upload_to="lessons", **NULLABLE)
    video_url = models.CharField(verbose_name="Ссылка на видео", max_length=200, **NULLABLE)
    course = models.ForeignKey(to=Course, related_name="lessons", on_delete=models.SET_NULL, **NULLABLE)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
