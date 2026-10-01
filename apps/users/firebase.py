import firebase_admin
from django.conf import settings
from firebase_admin import auth, credentials


def get_firebase_app():
    try:
        return firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(settings.FIREBASE_KEY_PATH)
        return firebase_admin.initialize_app(cred)


def verify_firebase_token(id_token: str):
    return auth.verify_id_token(
        id_token,
        app=get_firebase_app(),
        check_revoked=True,
    )
