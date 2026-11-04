import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or restore the PhilexFinancial owner account."

    def handle(self, *args, **options):
        username = os.environ.get("OWNER_USERNAME")
        email = os.environ.get("OWNER_EMAIL")
        password = os.environ.get("OWNER_PASSWORD")

        if not all([username, email, password]):
            self.stdout.write("Owner setup skipped: credentials not supplied.")
            return

        if len(password) < 12:
            raise CommandError("Owner password must contain at least 12 characters.")

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Owner account created." if created
                else "Owner account access restored."
            )
        )
