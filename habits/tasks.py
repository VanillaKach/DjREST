from celery import shared_task
from .models import Habit
from django.utils import timezone
from datetime import timedelta

@shared_task
def check_inactive_habits():
    now = timezone.now()
    habits = Habit.objects.filter(last_completed__lt=now - timedelta(days=7))

    for habit in habits:
        habit.delete()  # или отправить уведомление
