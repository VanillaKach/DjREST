from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Habit
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpass')
        self.habit = Habit.objects.create(
            user=self.user,
            place='Дома',
            time='12:00',
            action='Пробежка',
            is_pleasant=False,
            frequency=1,
            execution_time=60,
            is_public=False
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        url = '/api/habits/habits/'
        data = {
            'place': 'Парк',
            'time': '13:00',
            'action': 'Прогулка',
            'frequency': 1,
            'execution_time': 120,
            'is_public': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_my_habits(self):
        url = '/api/habits/habits/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_public_habits(self):
        url = '/api/habits/public/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_validate_last_completed(self):
        self.habit.last_completed = timezone.now() - timedelta(days=8)
        with self.assertRaises(Exception):
            self.habit.full_clean()
