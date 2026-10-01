import re

from django.contrib.auth import get_user_model
from firebase_admin import auth
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AccountDeletionRequest

User = get_user_model()


def issue_tokens(user: User) -> dict:
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def _generate_username(email: str) -> str:
    base = re.sub(r"[^a-z0-9_]", "_", email.split("@")[0].lower())[:27]
    username, counter = base, 1
    while User.objects.filter(username=username).exists():
        counter += 1
        username = f"{base}_{counter}"
    return username


def get_or_create_firebase_user(*, firebase_uid: str, email: str) -> tuple[User, bool]:
    username = _generate_username(email)
    user, created = User.objects.get_or_create(
        firebase_uid=firebase_uid,
        defaults={
            "username": username,
            "email": email,
            "display_name": username,
        },
    )
    return user, created


def get_user_data_deletion(user: User):
    data = AccountDeletionRequest.objects.get(user=user)
    return data


def verify_id_token(id_token: str):
    try:
        decoded = auth.verify_id_token(id_token, check_revoked=True)
    except auth.InvalidIdTokenError:
        raise AuthenticationFailed("id_token isnt right")

    if not decoded.get("email") or not decoded.get("uid"):
        raise ValidationError("email or uid isnt right")

    return decoded
