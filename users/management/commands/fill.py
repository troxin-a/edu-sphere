from datetime import date
from random import choice, randint
from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from edu.models import Course, Lesson
from users.models import Payment, User

chars = "qwertyuiopasdfghjklzxcvbnm"
digits = "1234567890"


class Command(BaseCommand):
    """
    Создает группу модераторов
    """

    def handle(self, *args, **kwargs) -> str | None:
        Group.objects.create(name="moderators")
        print('Создана группа "moderators"')
