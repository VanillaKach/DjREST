from rest_framework import serializers
from .models import Habit
from .validators import validate_associated_habit_and_reward, validate_pleasant_habit_for_association, validate_pleasant_habit_fields

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, attrs):
        validate_associated_habit_and_reward(attrs)
        if attrs.get('associated_habit'):
            validate_pleasant_habit_for_association(attrs['associated_habit'])
        if attrs.get('is_pleasant'):
            validate_pleasant_habit_fields(attrs)
        return attrs
