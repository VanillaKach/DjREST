from celery import shared_task
from .services import send_telegram_message
from habits.models import Habit
from datetime import datetime, timedelta

@shared_task
def send_habit_reminders():
    now = datetime.now().time()
    habits_due = Habit.objects.filter(time__lte=now, time__gte=(datetime.now() - timedelta(minutes=1)).time())

    for habit in habits_due:
        if habit.user.telegram_chat_id:
            message = f'Напоминание: пора выполнить привычку "{habit.action}" в {habit.place}!'
            send_telegram_message(habit.user.telegram_chat_id, message)
