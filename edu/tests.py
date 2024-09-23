from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from edu.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="user1@test.ru")
        self.user2 = User.objects.create(email="user2@test.ru")
        self.moderator = User.objects.create(email="moderator@test.ru")

        Group.objects.create(name="moderators")
        group_moderator = Group.objects.get(name="moderators")
        group_moderator.user_set.add(self.moderator)

        self.course1 = Course.objects.create(name="course1")
        self.lesson1 = Lesson.objects.create(name="lesson1", course=self.course1, owner=self.user1)

    def test_create_lessons(self):
        """Тест на создание урока"""

        url = reverse("education:create-lesson")
        data = {
            "name": "test",
            "description": "test",
            "owner": self.user2.id,
        }
        # Неавторизован
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Lesson.objects.count(), 1)
        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)
        # Пользователь
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.all().last().name, "test")

    def test_retrieve_lessons(self):
        """Тест на просмотр урока"""

        url = reverse("education:detail-lesson", args=(self.lesson1.pk,))
        data = {
            "id": self.lesson1.pk,
            "name": self.lesson1.name,
            "description": None,
            "preview": None,
            "video_url": None,
            "course": self.course1.pk,
            "owner": self.lesson1.owner.pk,
        }
        # Неавторизован
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Пользователь-НЕ-владелец
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)
        # Пользователь-владелец
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)

    def test_list_lessons(self):
        """Тест на просмотр списка уроков"""

        url = reverse("education:list-lesson")
        data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson1.pk,
                    "name": self.lesson1.name,
                    "description": None,
                    "preview": None,
                    "video_url": None,
                    "course": self.course1.pk,
                    "owner": self.lesson1.owner.pk,
                }
            ],
        }
        # Неавторизован
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)
        # Пользователь
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)

    def test_patch_lessons(self):
        """Тест на редактирование урока"""

        url = reverse("education:update-lesson", args=(self.lesson1.pk,))
        data1 = {
            "id": self.lesson1.pk,
            "name": "test-patch",
            "description": None,
            "preview": None,
            "video_url": None,
            "course": self.course1.pk,
            "owner": self.lesson1.owner.pk,
        }
        data2 = {
            "id": self.lesson1.pk,
            "name": "test-put",
            "description": None,
            "preview": None,
            "video_url": None,
            "course": self.course1.pk,
            "owner": self.lesson1.owner.pk,
        }
        # Неавторизован
        response = self.client.patch(url, {"name": "test-patch"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Пользователь-НЕ-владелец
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(url, {"name": "test-patch"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(url, {"name": "test-patch"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data1)
        # Пользователь-владелец
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(url, {"name": "test-patch"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data1)
        # Пользователь-владелец (PUT метод)
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(url, {"name": "test-put"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data2)

    def test_delete_lessons(self):
        """Тест на удаление урока"""

        url = reverse("education:destroy-lesson", args=(self.lesson1.pk,))
        # Неавторизован
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Пользователь-НЕ-владелец
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # # Пользователь-владелец
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
