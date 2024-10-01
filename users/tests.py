from datetime import date
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from edu.models import Course, Lesson, Subscription
from users.models import Payment, User


class UserTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="user1@test.ru")
        self.user2 = User.objects.create(email="user2@test.ru")
        self.moderator = User.objects.create(email="moderator@test.ru")

        Group.objects.create(name="moderators")
        group_moderator = Group.objects.get(name="moderators")
        group_moderator.user_set.add(self.moderator)

    def test_user_create(self):
        """Тест на регистрацию"""

        url = reverse("users:create-user")
        data = {
            "email": "test@test.ru",
            "password": "test",
        }
        data2 = {
            "email": "test2@test.ru",
            "password": "test",
        }
        # Неавторизован
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(response.json()["email"], "test@test.ru")
        # Авторизован
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url, data2, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 4)

    def test_user_detail(self):
        """Тест на просмотр пользователя"""

        url = reverse("users:detail-user", args=(self.user1.pk,))
        url_moderator = reverse("users:detail-user", args=(self.moderator.pk,))
        data_not_owner = {
            "id": self.user1.pk,
            "email": self.user1.email,
            "first_name": "",
        }
        data_for_moderator = {
            "id": self.user1.pk,
            "email": self.user1.email,
            "first_name": "",
            "last_name": "",
            "payments": [],
            "phone": None,
        }
        # Неавторизован
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Пользователь-НЕ-владелец профиля
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data_not_owner)
        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data_for_moderator)
        # Как модератор видит сам себя?
        response = self.client.get(url_moderator, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("password" in response.json().keys())
        # Пользователь-владелец профиля
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("password" in response.json().keys())

    def test_user_list(self):
        """Тест на просмотр списка пользователей"""

        url = reverse("users:list-user")
        # Неавторизован
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 3)
        self.assertTrue("payments" in response.json()["results"][0].keys())
        self.assertFalse("password" in response.json()["results"][0].keys())
        self.assertTrue("payments" in response.json()["results"][1].keys())
        self.assertFalse("password" in response.json()["results"][1].keys())
        self.assertTrue("payments" in response.json()["results"][2].keys())
        self.assertFalse("password" in response.json()["results"][2].keys())
        # Пользователь
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 3)
        self.assertFalse("payments" in response.json()["results"][1].keys())
        self.assertFalse("password" in response.json()["results"][1].keys())

    def test_user_update(self):
        """Тест на редактирование профиля пользователя"""

        url = reverse("users:update-user", args=(self.user1.pk,))
        # Неавторизован
        response = self.client.patch(url, {"last_name": "test-patch"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Пользователь-НЕ-владелец
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(url, {"last_name": "test-patch"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(url, {"last_name": "test-patch"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Пользователь-владелец
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(url, {"last_name": "test-patch"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["last_name"], "test-patch")

    def test_user_delete(self):
        """Тест на удаление пользователя"""

        url = reverse("users:destroy-user", args=(self.user1.pk,))
        # Неавторизован
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.count(), 3)
        # Пользователь-НЕ-владелец
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 3)
        # Пользователь-владелец
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 3)
        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)


class PaymentTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="user1@test.ru")
        self.user2 = User.objects.create(email="user2@test.ru")
        self.moderator = User.objects.create(email="moderator@test.ru")

        Group.objects.create(name="moderators")
        group_moderator = Group.objects.get(name="moderators")
        group_moderator.user_set.add(self.moderator)

        self.course1 = Course.objects.create(name="course1")
        self.lesson1 = Lesson.objects.create(name="lesson1", course=self.course1, owner=self.user1)

        self.pay2 = Payment.objects.create(
            user=self.user2,
            course=self.course1,
            amount=200,
            method="TF",
            date="2024-10-10",
        )
        self.pay1 = Payment.objects.create(
            user=self.user1,
            lesson=self.lesson1,
            amount=150,
            method="CH",
            date="2024-10-10",
        )

    def test_payments_list(self):
        """Тест на просмотр списка платежей"""

        data = [
            {
                "amount": self.pay1.amount,
                "course": None,
                "date": self.pay1.date,
                "id": self.pay1.id,
                "lesson": self.pay1.lesson.id,
                "method": self.pay1.method,
                "user": self.pay1.user.id,
                "session_id": self.pay1.session_id,
                "link": self.pay1.link,
            },
            {
                "amount": self.pay2.amount,
                "course": self.pay2.course.id,
                "date": self.pay2.date,
                "id": self.pay2.id,
                "lesson": None,
                "method": self.pay2.method,
                "user": self.pay2.user.id,
                "session_id": self.pay2.session_id,
                "link": self.pay2.link,
            },
        ]

        url = reverse("users:payments-list")
        # Неавторизован
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Пользователь
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"], data)
