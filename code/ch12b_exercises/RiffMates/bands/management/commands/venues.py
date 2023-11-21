# RiffMates/bands/management/commands/venues.py
from bands.models import Venue
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Lists registered venues"

    def add_arguments(self, parser):
        parser.add_argument(
            "--rooms",
            "-r",
            action="store_true",
            help="Display a venue's room information",
        )

    def handle(self, *args, **options):
        for venue in Venue.objects.all():
            self.stdout.write(venue.name)

            if options["rooms"]:
                for room in venue.room_set.all():
                    self.stdout.write("   " + room.name)
