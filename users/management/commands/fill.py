from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Создает группу модераторов
    """

    def handle(self, *args, **kwargs) -> str | None:
        Group.objects.create(name="moderators")
        print('Создана группа "moderators"')
