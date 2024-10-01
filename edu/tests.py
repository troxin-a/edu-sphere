from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from edu.models import Course, Lesson, Subscription
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
            "course": self.course1.id,
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
        self.assertEqual(Lesson.objects.all().first().name, "test")

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
        response = self.client.patch(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Пользователь-НЕ-владелец
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(url, {}, format="json")
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
        response = self.client.put(
            url,
            {
                "name": "test-put",
                "course": self.course1.pk,
            },
            format="json",
        )
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
        # Пользователь-владелец
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscribtionTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="user1@test.ru")
        self.course1 = Course.objects.create(name="course1")

    def test_subscribe_desubscribe_course(self):
        """Тест на подписку/отписку к курсу"""

        url = reverse("education:course-subscription")
        data = {
            "course": self.course1.id,
        }
        # Неавторизован
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Subscription.objects.count(), 0)

        # Пользователь ПОДПИСКА
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "подписка добавлена"})
        self.assertEqual(Subscription.objects.filter(user=self.user1).count(), 1)
        # Проверка на возвращаемый курс
        course_url = reverse("education:course-detail", args=(self.course1.id,))
        response = self.client.get(course_url, format="json")
        self.assertEqual(response.json()["is_subscribed"], "Вы подписаны")

        # Пользователь ОТПИСКА
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "подписка удалена"})
        self.assertEqual(Subscription.objects.filter(user=self.user1).count(), 0)
        # Проверка на возвращаемый курс
        course_url = reverse("education:course-detail", args=(self.course1.id,))
        response = self.client.get(course_url, format="json")
        self.assertEqual(response.json()["is_subscribed"], "Вы не подписаны")


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="user1@test.ru")
        self.user2 = User.objects.create(email="user2@test.ru")
        self.moderator = User.objects.create(email="moderator@test.ru")

        Group.objects.create(name="moderators")
        group_moderator = Group.objects.get(name="moderators")
        group_moderator.user_set.add(self.moderator)

        self.now = "2024-10-01T00:00:00Z"
        self.course1 = Course.objects.create(name="course1", owner=self.user1, updated_at=self.now)

    def test_create_course(self):
        """Тест на создание курса"""

        url = reverse("education:course-list")
        data = {
            "name": "test",
            "description": "test",
            "owner": self.user2.id,
        }
        # Неавторизован
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Course.objects.count(), 1)
        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Course.objects.count(), 1)
        # Пользователь
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url, {"name": "test", "description": "test"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Course.objects.all().first().name, "test")

    def test_retrieve_course(self):
        """Тест на просмотр урока"""

        url = reverse("education:course-detail", args=(self.course1.pk,))
        data = {
            "is_subscribed": "Вы не подписаны",
            "name": self.course1.name,
            "description": None,
            "preview": None,
            "count_lessons": 0,
            "owner": self.course1.owner.pk,
            "lessons": [],
            "updated_at": self.now,
        }
        # Неавторизован
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Пользователь любой (даже не владелец)
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)

    def test_list_course(self):
        """Тест на просмотр списка курсов"""

        url = reverse("education:course-list")
        data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "is_subscribed": "Вы не подписаны",
                    "name": self.course1.name,
                    "description": None,
                    "preview": None,
                    "count_lessons": 0,
                    "owner": self.course1.owner.pk,
                    "lessons": [],
                    "updated_at": self.now,
                }
            ],
        }
        # Неавторизован
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Пользователь любой (даже не владелец)
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)

    def test_patch_course(self):
        """Тест на редактирование курса"""

        url = reverse("education:course-detail", args=[self.course1.pk])
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
        self.assertEqual(response.json()["name"], "test-patch")
        # Пользователь-владелец
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(url, {"name": "test-patch"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "test-patch")
        # Пользователь-владелец (PUT метод)
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(url, {"name": "test-put"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "test-put")

    def test_delete_course(self):
        """Тест на удаление урока"""

        url = reverse("education:course-detail", args=(self.course1.pk,))
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
        # Пользователь-владелец
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
