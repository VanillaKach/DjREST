from django.core.exceptions import ValidationError

def validate_associated_habit_and_reward(value):
    # Проверяем, является ли value объектом модели или словарём
    if hasattr(value, 'get'):
        # Это словарь (например, attrs из сериализатора)
        associated_habit_val = value.get('associated_habit')
        reward_val = value.get('reward')
    else:
        # Это объект модели (например, self из модели)
        associated_habit_val = getattr(value, 'associated_habit', None)
        reward_val = getattr(value, 'reward', None)

    if associated_habit_val and reward_val:
        raise ValidationError('Нельзя одновременно указывать связанную привычку и вознаграждение.')

def validate_pleasant_habit_for_association(value):
    if value and not value.is_pleasant:
        raise ValidationError('Связанная привычка должна быть приятной.')

def validate_pleasant_habit_fields(value):
    # value - это attrs (словарь) в сериалайзере или self (объект модели) в clean
    if hasattr(value, 'get'):
        # Это словарь
        is_pleasant_val = value.get('is_pleasant')
        reward_val = value.get('reward')
        associated_habit_val = value.get('associated_habit')
    else:
        # Это объект модели
        is_pleasant_val = getattr(value, 'is_pleasant', False)
        reward_val = getattr(value, 'reward', None)
        associated_habit_val = getattr(value, 'associated_habit', None)

    if is_pleasant_val and (reward_val or associated_habit_val):
        raise ValidationError('Приятная привычка не может иметь вознаграждение или связанную привычку.')
