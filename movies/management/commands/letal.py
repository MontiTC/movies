from django.core.management.base import BaseCommand, CommandError
from movies.models import Movie
class Command(BaseCommand):
    help = "Creates a user"
    def handle(self, *args, **options):
         Movie.objects.all().delete()