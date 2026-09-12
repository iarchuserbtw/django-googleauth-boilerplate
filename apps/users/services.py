# users/services.py
import re
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def _generate_username(email: str) -> str:
    base = re.sub(r'[^a-z0-9_]', '_', email.split('@')[0].lower())[:27]
    username, counter = base, 1
    while User.objects.filter(username=username).exists():
        counter += 1
        username = f'{base}_{counter}'
    return username


def get_or_create_firebase_user(*, firebase_uid: str, email: str,
                                display_name: str) -> tuple[User, bool]:
    user, created = User.objects.get_or_create(
        firebase_uid=firebase_uid,
        defaults={
            'username': _generate_username(email),
            'email': email,
            'display_name': display_name or '',
        },
    )
    return user, created


def issue_tokens(user: User) -> dict:
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}