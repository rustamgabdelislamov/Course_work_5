from datetime import time
from unittest import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from habit.models import Habits
from habit.validators import validate_pleasant_habit
from users.models import CustomUser


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email="test@mail.ru", password=1990)
        self.habit = Habits.objects.create(
            action="Рубить дрова",
            owner=self.user,
            reward_action=False,
            time=time(14, 30),
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habit:habit_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        url = reverse("habit:habit_create")
        data = {
            "action": "Пилить бревно",
            "owner": self.user.pk,
            "reward_action": False,
            "time": "14:20:00",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.all().count(), 2)

    def test_habit_update(self):
        url = reverse("habit:habit_update", args=(self.habit.pk,))
        data = {
            "action": "Пилить сук",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Пилить сук")

    def test_habit_delete(self):
        url = reverse("habit:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habits.objects.all().count(), 0)

    #
    #
    def test_habit_list(self):
        url = reverse("habit:habit_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "place": None,
                    "action": self.habit.action,
                    "time": "14:30:00",
                    "reward_action": False,
                    "addition_habit": None,
                    "period": 1,
                    "award": None,
                    "time_to_action": "00:02:00",
                    "is_published": True,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(data, result)

    def test_habit_retrieve_unauthenticated(self):
        self.client.force_authenticate(user=None)  # разлогиниваем
        url = reverse("habit:habit_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_habit_update_as_is_staff_only_update_is_published(self):
        # Создаем админа, который может менять только публикацию
        user = CustomUser.objects.create(email="admin@mail.ru", is_staff=True)

        # Аутентифицируемся как админ
        self.client.force_authenticate(user=user)

        url = reverse("habit:habit_update", args=(self.habit.pk,))
        data = {"is_published": False}
        response = self.client.patch(url, data)
        self.assertEqual(self.habit.is_published, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.is_published, False)

        data = {"action": "Топить баню"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Рубить дрова")


# class HabitValidatorsTestCase(APITestCase):
#
#     def setUp(self):
#         self.user = CustomUser.objects.create(email="test@mail.ru", password=1990)
#
#         # связанная привычка
#         self.related_habit = Habits.objects.create(
#             action='Чистить зубы',
#             owner=self.user,
#             reward_action=True,
#             time=time(8, 0)
#         )
#         # основная привычка
#         self.habit = Habits.objects.create(
#             action="Рубить дрова",
#             owner=self.user,
#             reward_action=False,
#             addition_habit=self.related_habit,
#             time=time(14, 30),
#         )
#         self.client.force_authenticate(user=self.user)
#
#     def test_validate_pleasant_habit_with_valid_habit(self):
#         validate_pleasant_habit()

# def test_validate_pleasant_habit_with_invalid_habit(self):
#     # Создайте объект привычки без признака приятной привычки
#     addition_habit = Habits(reward_action=False)  # Замените на вашу модель
#     with self.assertRaises(ValidationError):
#         validate_pleasant_habit(addition_habit)
#
# def test_validate_pleasant_habit_with_none(self):
#     # Проверяем, что None не вызывает исключение
#     addition_habit = None
#     try:
#         validate_pleasant_habit(addition_habit)
#     except ValidationError:
#         self.fail("validate_pleasant_habit() raised ValidationError unexpectedly for None!")


#     def test_lesson_update_as_moderator(self):
#         # Создаем пользователся модератора и добавляем его в группу "moders"
#         moderator = CustomUser.objects.create(email='moderator@mail.ru')
#         self.group_moders, _ = Group.objects.get_or_create(name="moders")
#         # Получаем группу moders
#         group_moders = Group.objects.get(name='moders')
#         # Добавляем пользователя в группу
#         moderator.groups.add(group_moders)
#         # Аутентифицируемся как модератор
#         self.client.force_authenticate(user=moderator)
#
#         url = reverse("materials:lesson_update", args=(self.lesson.pk,))
#         data = {"name": "Физика"}
#         response = self.client.patch(url, data)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.lesson.refresh_from_db()
#         self.assertEqual(self.lesson.name, "Физика")
