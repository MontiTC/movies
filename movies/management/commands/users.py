from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
class Command(BaseCommand):
    help = "Creates a user"
    def handle(self, *args, **options):
        user = User.objects.create_user(username='Monti', password='123')