from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.users.models import AccountDeletionRequest

User = get_user_model()


class AccountDeletionRequestTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            firebase_uid="firebase-123",
        )

    def test_schedule_creates_deletion_request(self):
        request = AccountDeletionRequest.schedule(
            self.user,
            reason="test reason",
        )

        self.assertEqual(request.user, self.user)
        self.assertEqual(request.reason, "test reason")
        self.assertFalse(request.is_cancelled)

    def test_schedule_deactivates_user(self):
        AccountDeletionRequest.schedule(self.user)

        self.user.refresh_from_db()

        self.assertFalse(self.user.is_active)

    def test_schedule_sets_delete_at(self):
        before = timezone.now() + timedelta(days=7)

        request = AccountDeletionRequest.schedule(self.user)

        after = timezone.now() + timedelta(days=7)

        self.assertGreaterEqual(request.delete_at, before)
        self.assertLessEqual(request.delete_at, after)

    def test_cancel_reactivates_user(self):
        request = AccountDeletionRequest.schedule(self.user)

        request.cancel()

        self.user.refresh_from_db()
        request.refresh_from_db()

        self.assertTrue(self.user.is_active)
        self.assertTrue(request.is_cancelled)

    def test_second_schedule_updates_existing_request(self):
        first = AccountDeletionRequest.schedule(
            self.user,
            reason="first",
        )

        second = AccountDeletionRequest.schedule(
            self.user,
            reason="second",
        )

        self.assertEqual(first.pk, second.pk)
        self.assertEqual(second.reason, "second")
