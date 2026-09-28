from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import AccountDeletionRequest

User = get_user_model()


class AccountDeletionAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            firebase_uid="firebase-123",
        )

        access = RefreshToken.for_user(self.user).access_token

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access}"
        )

    @patch("apps.users.views.verify_id_token")
    def test_request_account_deletion(self, mock_verify):
        mock_verify.return_value = {
            "uid": "firebase-123",
            "email": "test@example.com",
        }

        response = self.client.post(
            reverse("delete_user"),
            {
                "id_token": "fake-token",
                "reason": "Testing",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request = AccountDeletionRequest.objects.get(
            user=self.user
        )

        self.assertEqual(request.reason, "Testing")

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    @patch("apps.users.views.verify_id_token")
    def test_cannot_delete_with_another_users_firebase_token(
        self,
        mock_verify,
    ):
        mock_verify.return_value = {
            "uid": "someone-else",
            "email": "other@example.com",
        }

        response = self.client.post(
            reverse("delete_user"),
            {
                "id_token": "fake-token",
                "reason": "",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertFalse(
            AccountDeletionRequest.objects.filter(
                user=self.user
            ).exists()
        )

class CancelDeletionAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            firebase_uid="firebase-123",
        )

        AccountDeletionRequest.schedule(self.user)

    @patch("apps.users.views.verify_id_token")
    def test_cancel_deletion(self, mock_verify):
        mock_verify.return_value = {
            "uid": "firebase-123",
            "email": "test@example.com",
        }

        response = self.client.post(
            reverse("cancel_delete_user"),
            {"id_token": "fake-token"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

        request = AccountDeletionRequest.objects.get(
            user=self.user
        )

        self.assertTrue(request.is_cancelled)