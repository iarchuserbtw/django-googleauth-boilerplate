from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            display_name="testuser",
            email="test@example.com",
            firebase_uid="firebase-123",
        )

        access = RefreshToken.for_user(self.user).access_token

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access}"
        )

    def test_get_profile(self):
        response = self.client.get(
            reverse("me_view")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["username"],
            "testuser",
        )

    def test_update_profile(self):
        response = self.client.patch(
            reverse("me_view"),
            {
                "username": "newusername",
                "display_name": "newname",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.username,
            "newusername",
        )

    def test_email_cannot_be_changed(self):
        self.client.patch(
            reverse("me_view"),
            {"email": "hacker@example.com"},
            format="json",
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.email,
            "test@example.com",
        )

    def test_unauthenticated_user_cannot_get_profile(self):
        self.client.credentials()

        response = self.client.get(
            reverse("me_view")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )