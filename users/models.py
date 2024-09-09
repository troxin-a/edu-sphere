from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="Почта", unique=True)
    phone = models.CharField(verbose_name="Телефон", max_length=25, **NULLABLE)
    city = models.CharField(verbose_name="Город", max_length=100, **NULLABLE)
    avatar = models.ImageField(verbose_name="Аватар", upload_to="users", **NULLABLE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name = "Пользователи"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
