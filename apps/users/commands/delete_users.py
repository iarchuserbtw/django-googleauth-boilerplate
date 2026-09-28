from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.users.models import AccountDeletionRequest


class Command(BaseCommand):
    help = "Delete expired accounts"

    def handle(self, *args, **options):
        requests = AccountDeletionRequest.objects.filter(
            delete_at__lte=timezone.now(),
            is_cancelled=False,
        ).select_related("user")

        for deletion_request in requests:
            user = deletion_request.user

            # TODO: удалить пользователя из Firebase
            user.delete()

            self.stdout.write(
                self.style.SUCCESS("Account deleted")
            )