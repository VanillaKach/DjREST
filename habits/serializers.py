from rest_framework import serializers
from .models import Habit
from .validators import (
    validate_associated_habit_and_reward,
    validate_pleasant_habit_for_association,
    validate_pleasant_habit_fields
)

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        # Исключаем 'user' из сериализуемых полей, передаваемых в validate
        exclude = ['user']

    def validate(self, attrs):
        # Проверки проводим на словаре attrs
        validate_associated_habit_and_reward(attrs)
        if attrs.get('associated_habit'):
            # validate_pleasant_habit_for_association ожидает объект модели, но в сериалайзере associated_habit - это объект или None
            # Это должно работать, если associated_habit - действительный экземпляр модели Habit
            validate_pleasant_habit_for_association(attrs['associated_habit'])
        if attrs.get('is_pleasant'):
            validate_pleasant_habit_fields(attrs)
        return attrs
