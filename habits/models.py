from django.db import models
from django.core.exceptions import ValidationError
from users.models import CustomUser

def validate_associated_habit_and_reward(value):
    if value.associated_habit and value.reward:
        raise ValidationError('Нельзя одновременно указывать связанную привычку и вознаграждение.')

def validate_execution_time(value):
    if value > 120:
        raise ValidationError('Время выполнения не должно превышать 120 секунд.')

def validate_pleasant_habit_for_association(value):
    if value and not value.is_pleasant:
        raise ValidationError('Связанная привычка должна быть приятной.')

def validate_pleasant_habit_fields(value):
    if value.is_pleasant and (value.reward or value.associated_habit):
        raise ValidationError('Приятная привычка не может иметь вознаграждение или связанную привычку.')

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

    def clean(self):
        if self.associated_habit:
            validate_associated_habit_and_reward(self)
            validate_pleasant_habit_for_association(self.associated_habit)
        if self.is_pleasant:
            validate_pleasant_habit_fields(self)

    def __str__(self):
        return f'{self.user.email}: {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
