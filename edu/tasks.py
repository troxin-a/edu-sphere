from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email_about_course_update(subject, body, emails):

    email = EmailMessage(
        subject=subject,
        body=body,
        to=emails,
    )

    email.send(fail_silently=False)
