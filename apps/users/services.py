from django.contrib.auth import get_user_model

import firebase_admin
from firebase_admin import credentials

import re


User = get_user_model()


def _generate_username(email: str) -> str:
    """ivan.petrov@gmail.com → ivan_petrov; при коллизии → ivan_petrov_2"""
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
    
cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred)

def get_token(user_id): ...