from django.core.exceptions import ValidationError

def validate_associated_habit_and_reward(attrs):
    if attrs.get('associated_habit') and attrs.get('reward'):
        raise ValidationError('Нельзя одновременно указывать связанную привычку и вознаграждение.')

def validate_pleasant_habit_for_association(value):
    if value and not value.is_pleasant:
        raise ValidationError('Связанная привычка должна быть приятной.')

def validate_pleasant_habit_fields(attrs):
    if attrs.get('is_pleasant') and (attrs.get('reward') or attrs.get('associated_habit')):
        raise ValidationError('Приятная привычка не может иметь вознаграждение или связанную привычку.')
