from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    ''' Менеджер при создании пользователей'''
    
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_google_user(self, google_id, email):
        user = self.model(google_id=google_id, email=email)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(
            phone=phone,
            password=password,
            **extra_fields
        )

class User(AbstractBaseUser, PermissionsMixin):
    ''' Стандартная модель пользователя'''
    
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    display_name = models.CharField(max_length=25, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone