from auth_api.models import Profile
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Generate user for test"

    def handle(self, *args, **options):
        user = User.objects.create_user(username="raphael@local.test", email="raphael@local.test", password="user")
        Profile.objects.create(user=user)
        user = User.objects.create_user(username="jules@local.test", email="jules@local.test", password="user")
        Profile.objects.create(user=user)
        user = User.objects.create_superuser("admin@local.test", "admin@local.test", "admin")
        Profile.objects.create(user=user)
        self.stdout.write(self.style.SUCCESS("OK"))
