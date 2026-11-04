import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Safely create or restore the PhilexFinancial owner account."

    def handle(self, *args, **options):
        username = os.environ.get("OWNER_USERNAME")
        email = os.environ.get("OWNER_EMAIL")
        password = os.environ.get("OWNER_PASSWORD")
        confirmation = os.environ.get("OWNER_SETUP_CONFIRM")

        if confirmation != "YES":
            self.stdout.write("Owner setup skipped: confirmation not supplied.")
            return

        if not all([username, email, password]):
            raise CommandError("Owner setup requires all three credentials.")

        if len(password) < 12:
            raise CommandError("Owner password must contain at least 12 characters.")

        User = get_user_model()

        try:
            user = User.objects.get(username=username)
            created = False
        except User.DoesNotExist:
            user = User(username=username)
            created = True

        if not created and not user.is_superuser:
            raise CommandError(
                "This username already belongs to a non-owner account. "
                "No account was changed."
            )

        user.email = email
        validate_password(password, user)

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        message = "Owner account created." if created else "Owner account restored."
        self.stdout.write(self.style.SUCCESS(message))
