from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, *, username, email, password=None,
                    firebase_uid=None, display_name='', **extra_fields):
        if not username:
            raise ValueError('User must have a username')
        if not email:
            raise ValueError('User must have an email')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            firebase_uid=firebase_uid,
            display_name=display_name,
            **extra_fields,
        )
        user.set_password(password)  # None → unusable, google-юзер не войдёт по паролю
        user.save(using=self._db)
        return user

    def create_superuser(self, *, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(
            username=username, email=email, password=password, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    ''' Стандартная модель пользователя'''
    
    username = models.CharField(max_length=30, unique=True)

    firebase_uid = models.CharField(max_length=128, unique=True, null=True, blank=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    
    display_name = models.CharField(max_length=25, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username