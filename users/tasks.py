from django.utils import timezone
from celery import shared_task

from users.models import Payment, User
from users.services import get_session


@shared_task
def disable_inactive_users():
    """
    Отключает пользователей (is_active),
    которые не логинились более 30 дней"""

    deltatime = timezone.now() - timezone.timedelta(days=30)

    users = User.objects.filter(is_staff=False, is_superuser=False, is_active=True, last_login__lt=deltatime)

    if users:
        for user in users:
            user.is_active = False
        User.objects.bulk_update(users, ["is_active"])


@shared_task
def check_payments():
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
            payment.date = timezone.now()
            payment.save()
