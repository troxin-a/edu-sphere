from django.utils import timezone
from edu.models import Course, Subscription
from edu.tasks import send_email_about_course_update


def update_course(course_id):
    """
    Функция обновляет дату последнего изменения и запускает отправку емейлов подписчикам,
    если с момента последнего изменения курса прошло более 4 часов.
    """

    course = Course.objects.filter(pk=course_id).first()
    previous_updated_at = course.updated_at
    course.updated_at = timezone.now()
    course.save(update_fields=["updated_at"])

    if course.updated_at - previous_updated_at > timezone.timedelta(seconds=4):
        subscriptions = Subscription.objects.filter(course=course_id)
        emails = [sub.user.email for sub in subscriptions]

        send_email_about_course_update.delay("Тема", "Письмо", emails)
