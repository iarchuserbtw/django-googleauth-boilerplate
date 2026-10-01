from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.users.services import (
    get_or_create_user,
    verify_id_token,
)

User = get_user_model()


class FirebaseUserServiceTests(TestCase):
    def test_creates_new_user(self):
        user, created = get_or_create_user(
            firebase_uid="uid-123",
            email="hello@example.com",
        )

        self.assertTrue(created)
        self.assertEqual(user.firebase_uid, "uid-123")
        self.assertEqual(user.email, "hello@example.com")
        self.assertEqual(user.username, "hello")
        self.assertEqual(user.display_name, "hello")

    def test_existing_user_is_not_created_twice(self):
        first, _ = get_or_create_user(
            firebase_uid="uid-123",
            email="hello@example.com",
        )

        second, created = get_or_create_user(
            firebase_uid="uid-123",
            email="hello@example.com",
        )

        self.assertFalse(created)
        self.assertEqual(first.pk, second.pk)

    def test_duplicate_username_gets_suffix(self):
        User.objects.create_user(
            username="hello",
            email="another@example.com",
        )

        user, _ = get_or_create_user(
            firebase_uid="uid-123",
            email="hello@example.com",
        )

        self.assertNotEqual(user.username, "hello")


class VerifyIdTokenTests(TestCase):
    @patch("apps.users.services.verify_firebase_token")
    def test_valid_token_returns_decoded_data(self, mock_verify):
        mock_verify.return_value = {
            "uid": "uid-123",
            "email": "hello@example.com",
        }

        decoded = verify_id_token("token")

        self.assertEqual(decoded["uid"], "uid-123")
        mock_verify.assert_called_once_with("token")

    @patch("apps.users.services.auth.verify_id_token")
    def test_missing_uid_raises_validation_error(self, mock_verify):
        mock_verify.return_value = {
            "email": "hello@example.com",
        }

        with self.assertRaises(ValidationError):
            verify_id_token("token")

    @patch("apps.users.services.auth.verify_id_token")
    def test_missing_email_raises_validation_error(self, mock_verify):
        mock_verify.return_value = {
            "uid": "uid-123",
        }

        with self.assertRaises(ValidationError):
            verify_id_token("token")
