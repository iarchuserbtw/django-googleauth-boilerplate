from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)

    first_name = None
    last_name = None

    email = models.EmailField(unique=True, null=True, blank=True)

    firebase_uid = models.CharField(max_length=128, unique=True, null=True, blank=True)
    display_name = models.CharField(max_length=25, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(blank=True, null=True)

    def get_full_name(self):
        return self.display_name or self.username

    def get_short_name(self):
        return self.username


class AccountDeletionRequest(models.Model):
    ''' Модель для удаление пользователей '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='deletion_request',
    )
    reason = models.TextField(blank=True)
    delete_at = models.DateTimeField(db_index=True)
    is_cancelled = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Запрос на удаление аккаунта'
        verbose_name_plural = 'Запросы на удаление аккаунтов'

    @classmethod
    def schedule(cls, user, reason='', days: int = 7):
        req, _ = cls.objects.update_or_create(
            user=user,
            defaults={
                'delete_at': timezone.now() + timedelta(days=days),
                'is_cancelled': False,
                'reason': reason,
            },
        )
        user.is_active = False
        user.save(update_fields=['is_active'])
        return req

    def cancel(self):
        self.is_cancelled = True
        self.save(update_fields=['is_cancelled'])
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
    