from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"

    # def ready(self):
    #     if not firebase_admin._apps:
    #         cred = credentials.Certificate(settings.FIREBASE_KEY_PATH)
    #         firebase_admin.initialize_app(cred)
