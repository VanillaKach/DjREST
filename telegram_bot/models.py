from django.db import models
from users.models import CustomUser

class TelegramUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    chat_id = models.CharField(max_length=50, verbose_name='Chat ID')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return f'{self.user.email} - {self.chat_id}'

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'
