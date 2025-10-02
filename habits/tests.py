from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from habits.models import Habit

User = get_user_model()


class HabitCreateTestCase(APITestCase):
    def setUp(self):
        """Создание пользователя и 2-х привычек, публичной и не приятной"""
        self.user = User.objects.create(email="sample@example.ru")
        self.user.set_password("testpass123")
        self.user.save()


        self.habit_1 = Habit.objects.create(
            owner=self.user,
            place="Кухня",
            time="10:00:00",
            action="Попить кофе",
            pleasantness=True,
            periodicity=1,
            time_to_complete="00:02:00",
            is_public=False,
        )


        self.habit_2 = Habit.objects.create(
            owner=self.user,
            place="Спальня",
            time="10:05:00",
            action="Отжимания",
            pleasantness=False,
            related_habit=self.habit_1,
            periodicity=1,
            time_to_complete="00:02:00",
            is_public=True,
        )

        self.client.force_authenticate(user=self.user)

    def test_habits_list_public(self):
        """Тест доступности списка публичных привычек"""
        url = reverse('habits:public-habits-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['action'], 'Отжимания')

    def test_habits_validation(self):
        """Тест валидации создания привычки"""
        url = reverse('habits:habit-create')
        data = {
            "place": "Тестовое место",
            "time": "10:00:00",
            "action": "Тестовое действие",
            "pleasantness": False,
            "periodicity": 1,
            "reward": "Конфета",
            "related_habit": self.habit_1.id,
            "time_to_complete": "00:01:00",
            "is_public": True,
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        self.assertIn('non_field_errors', response.data)
        self.assertIn(
            'Нужно указать либо связанную привычку, либо вознаграждение',
            str(response.data['non_field_errors'])
        )


class HabitsWithoutAuthorizationTest(APITestCase):
    def test_create_habit_unauthorized_fails(self):
        """Тест создания привычки не авторизованным пользователем"""
        url = reverse('habits:habit-create')
        data = {
            "place": "test",
            "time": "09:05:00",
            "action": "test",
            "pleasantness": True,
            "reward": "Конфета",
            "periodicity": 1,
            "time_to_complete": "00:02:00",
            "is_public": True
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Habit.objects.filter(action="test").exists())

