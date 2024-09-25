from datetime import datetime
from django.core.management import BaseCommand

from users.models import Payment
from users.services import get_session


class Command(BaseCommand):
    """Проверяет оплаченные сессии и вносит изменения в базу"""

    def handle(self, *args, **kwargs) -> str | None:
        payments = Payment.objects.filter(date=None)
        print(payments.count())

        for payment in payments:
            if not payment.session_id:
                continue

            session = get_session(payment.session_id)
            if not session:
                continue

            if session.get("status") == "complete":
                payment.link = ""
                payment.date = datetime.now()
                payment.save()
