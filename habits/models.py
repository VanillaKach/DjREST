from django.db import models
from django.core.exceptions import ValidationError
from users.models import CustomUser
from datetime import timedelta
from django.utils import timezone

# --- Импортируем универсальные валидаторы ---
from .validators import (
    validate_associated_habit_and_reward,
    validate_pleasant_habit_for_association,
    validate_pleasant_habit_fields
)

def validate_execution_time(value):
    if value > 120:
        raise ValidationError('Время выполнения не должно превышать 120 секунд.')

def validate_frequency(value):
    if value > 7:
        raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней.')

class Habit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.CharField(max_length=200, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=200, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    associated_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Связанная привычка')
    frequency = models.PositiveIntegerField(default=1, validators=[validate_frequency], verbose_name='Периодичность (в днях)')
    reward = models.CharField(max_length=200, blank=True, null=True, verbose_name='Вознаграждение')
    execution_time = models.PositiveIntegerField(validators=[validate_execution_time], verbose_name='Время на выполнение (в секундах)')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')
    last_completed = models.DateTimeField(null=True, blank=True, verbose_name='Последнее выполнение')

    def clean(self):
        super().clean()
        # Проверка, что прошло не более 7 дней с последнего выполнения
        if self.last_completed:
            if (timezone.now() - self.last_completed).days > 7:
                raise ValidationError('Привычка не может быть неактивной более 7 дней.')

        # Вызов других проверок
        # validate_associated_habit_and_reward ожидает объект модели
        validate_associated_habit_and_reward(self)
        if self.associated_habit:
            validate_pleasant_habit_for_association(self.associated_habit)
        if self.is_pleasant:
            # validate_pleasant_habit_fields ожидает объект модели
            validate_pleasant_habit_fields(self)

    def save(self, *args, **kwargs):
        # Вызываем clean перед сохранением
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.email}: {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
