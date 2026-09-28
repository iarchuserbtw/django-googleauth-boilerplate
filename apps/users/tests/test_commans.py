from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from apps.users.models import AccountDeletionRequest

User = get_user_model()


class DeleteUsersCommandTests(TestCase):
    def create_user(self, username):
        return User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            firebase_uid=f"firebase-{username}",
        )

    def test_expired_account_is_deleted(self):
        user = self.create_user("expired")

        request = AccountDeletionRequest.schedule(user)

        request.delete_at = (
            timezone.now() - timedelta(hours=1)
        )
        request.save(update_fields=["delete_at"])

        call_command("deleteusers")

        self.assertFalse(
            User.objects.filter(pk=user.pk).exists()
        )

    def test_future_account_is_not_deleted(self):
        user = self.create_user("future")

        AccountDeletionRequest.schedule(user)

        call_command("deleteusers")

        self.assertTrue(
            User.objects.filter(pk=user.pk).exists()
        )

    def test_cancelled_account_is_not_deleted(self):
        user = self.create_user("cancelled")

        request = AccountDeletionRequest.schedule(user)

        request.delete_at = (
            timezone.now() - timedelta(hours=1)
        )
        request.is_cancelled = True

        request.save(
            update_fields=[
                "delete_at",
                "is_cancelled",
            ]
        )

        call_command("deleteusers")

        self.assertTrue(
            User.objects.filter(pk=user.pk).exists()
        )

    def test_command_outputs_success_message(self):
        user = self.create_user("output")

        request = AccountDeletionRequest.schedule(user)

        request.delete_at = (
            timezone.now() - timedelta(hours=1)
        )
        request.save(update_fields=["delete_at"])

        stdout = StringIO()

        call_command(
            "deleteusers",
            stdout=stdout,
        )

        self.assertIn(
            "Account deleted",
            stdout.getvalue(),
        )