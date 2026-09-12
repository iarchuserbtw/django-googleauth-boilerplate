import firebase_admin
from firebase_admin import credentials
from django.apps import AppConfig
from django.conf import settings


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.users'

    def ready(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.FIREBASE_KEY_PATH)
            firebase_admin.initialize_app(cred)
