from datetime import date
from random import choice, randint
from django.core.management import BaseCommand

from edu.models import Course, Lesson
from users.models import Payment, User

chars = "qwertyuiopasdfghjklzxcvbnm"
digits = "1234567890"


class Command(BaseCommand):
    '''
    Заполняет:
      100 пользователей,
      100 платежей,
      10 курсов,
      25 уроков
    '''
    
    def handle(self, *args, **kwargs) -> str | None:

        users = []
        for _ in range(100):
            name_domain = lambda: [choice(chars) for _ in range(randint(5, 10))]
            email =  "".join(name_domain() + ["@"] + name_domain() + [choice([".ru", ".com"])])
            phone = "".join(["+79"] + [choice(digits) for _ in range(8)])
            users.append(User(email=email, phone=phone))
        User.objects.bulk_create(users)
        print("Пользователи заполнены")

        courses = [Course(name=f"{i} курс", description=f"Описание {i} курса") for i in range(1, 11)]
        Course.objects.bulk_create(courses)
        print("Курсы заполнены")

        lessons = []
        for i in range(1, 26):
            name = f"{i} урок"
            description=f"Описание {i} урока"
            course = Course.objects.get(pk=randint(1, 10))
            lessons.append(Lesson(name=name, description=description, course=course))
        Lesson.objects.bulk_create(lessons)
        print("Уроки заполнены")

        payments = []
        for i in range(1, 100):
            for _ in range(randint(1, 5)):
                user = User.objects.get(pk=i)
                date_pay = date(2024, randint(1, 12), randint(1, 28))
                if choice([True, False]):
                    lesson = Lesson.objects.get(pk=randint(1, 25))
                    course = None
                else:
                    course = Course.objects.get(pk=randint(1, 10))
                    lesson = None
                amount = randint(10, 300) * 100
                method = choice(["CH", "TF"])

                payments.append(Payment(
                    user = user,
                    lesson = lesson,
                    course = course,
                    amount = amount,
                    method = method,
                    date = date_pay
                ))
        Payment.objects.bulk_create(payments)
        print("Платежи заполнены")
