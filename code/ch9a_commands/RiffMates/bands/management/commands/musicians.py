# RiffMates/bands/management/commands/musicians.py
from bands.models import Musician
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Lists registered musicians"

    def handle(self, *args, **options):
        for musician in Musician.objects.all():
            self.stdout.write(f"{musician.last_name}, {musician.first_name}")
