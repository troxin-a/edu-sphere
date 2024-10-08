from django.contrib.auth.models import AbstractUser
from django.db import models

from edu.models import Course, Lesson


NULLABLE = {"blank": True, "null": True}
CASH = "CH"
TRANSFER = "TF"
PAYMENT_METHODS = [
    (CASH, "Наличные"),
    (TRANSFER, "Перевод на счет"),
]


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
        ordering = ["-id"]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    user = models.ForeignKey(
        to=User, verbose_name="Пользователь", on_delete=models.DO_NOTHING, related_name="payments", **NULLABLE
    )
    date = models.DateField(verbose_name="Дата оплаты", **NULLABLE)
    course = models.ForeignKey(
        to=Course, verbose_name="Оплаченный курс", on_delete=models.DO_NOTHING, related_name="paid_courses", **NULLABLE
    )
    lesson = models.ForeignKey(
        to=Lesson, verbose_name="Оплаченный урок", on_delete=models.DO_NOTHING, related_name="paid_lessons", **NULLABLE
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    method = models.CharField(max_length=2, verbose_name="Способ оплаты", choices=PAYMENT_METHODS)
    session_id = models.CharField(max_length=400, verbose_name="id сессии", **NULLABLE)
    link = models.URLField(max_length=400, verbose_name="Ссылка на оплату", **NULLABLE)

    def __str__(self):
        return f"{self.amount} - {self.user}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name = "Платежи"
        ordering = ["-id"]
