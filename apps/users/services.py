import re

from django.contrib.auth import get_user_model
from firebase_admin import auth
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def issue_tokens(user: User) -> dict:
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


def _generate_username(email: str) -> str:
    base = re.sub(r'[^a-z0-9_]', '_', email.split('@')[0].lower())[:27]
    username, counter = base, 1
    while User.objects.filter(username=username).exists():
        counter += 1
        username = f'{base}_{counter}'
    return username


def get_or_create_firebase_user(*, firebase_uid: str, email: str) -> tuple[User, bool]:
    user, created = User.objects.get_or_create(
        firebase_uid=firebase_uid,
        defaults={
            'username': _generate_username(email),
            'email': email,
            'display_name': _generate_username(email),
        },
    )
    return user, created


def verify_id_token(id_token: str):
    try:
        decoded = auth.verify_id_token(id_token, check_revoked=True)
    except auth.InvalidIdTokenError:
        raise ...

    if not decoded.get('email') or decoded.get('uid'):
            raise ...

    print(decoded)
    return decoded

    
if __name__ == '__main__':
    from firebase_admin import credentials

    cred = credentials.Certificate('firebase-credentials.json')
    firebase_admin.initialize_app(cred)

    id_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjY2MmQ3YTBkNGVlZmQzNDMyNjFjYWRkZmZhZWM2MjNkYzZjYTlmZjAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGVzdC1wcm9qZWN0LWVjOTczIiwiYXVkIjoidGVzdC1wcm9qZWN0LWVjOTczIiwiYXV0aF90aW1lIjoxNzg5NDY2ODMzLCJ1c2VyX2lkIjoiNVNVYjBINGpLdWNqRUR1dGd0TGtZbllyVHE2MyIsInN1YiI6IjVTVWIwSDRqS3VjakVEdXRndExrWW5ZclRxNjMiLCJpYXQiOjE3ODk0NjY4MzMsImV4cCI6MTc4OTQ3MDQzMywiZW1haWwiOiJ0ZXN0MTIyMzU2QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ0ZXN0MTIyMzU2QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.BRx_Jz3QismOg8D4L0XD9-yYrl-FvWThvQzpM7MJXVZpmh4yUs9AUQ0QB1i1zf5g494vff7JiBebbPls9sjLzLVbsLSxpA-X2iDIzK0pZDj6Fbb_-mJnQzwLzqLPx-mZLI3Y3UGksAKivcMxnA5_n2c0kVUJvLRTDYbXxKkPCq773CHPBjvT24dwoFvzqvAjaJce4RahI-zVT3k8QEw3P-VQznwYK_cq83hFUYNfDSJrm61tSykIFDZcTHk1Ab15-oHFpTy3N_wxTNP0Pf2eHr8oHNLRHB6KBXj4D_ZgD2xJz9jvhug2TNUf6QrAwdIQczBQxv_UJrM2KzuhY_nbzw'
    verify_id_token(id_token)

