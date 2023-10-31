# RiffMates/bands/management/commands/cleanup.py
from pathlib import Path

from bands.models import Musician, Venue
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Removes uploaded files not owned by a Musician or Venue"

    def add_arguments(self, parser):
        parser.add_argument(
            "--show",
            "-s",
            action="store_true",
            help=("Show which files would be removed but don't remove them"),
        )

    def handle(self, *args, **options):
        model_set = set()
        for musician in Musician.objects.all():
            if musician.picture:
                model_set.add(Path(musician.picture.path))

        for venue in Venue.objects.all():
            if venue.picture:
                model_set.add(Path(venue.picture.path))

        file_set = set(settings.MEDIA_ROOT.glob("**/*"))

        orphaned = file_set.difference(model_set)

        if not orphaned:
            self.stdout.write("No orphaned files")
            exit()

        if options["show"]:
            self.stdout.write(f"Orphaned files: ({len(orphaned)})")
            for path in orphaned:
                if path.is_file():
                    self.stdout.write("   " + str(path))
        else:
            self.stdout.write(f"Removing: ({len(orphaned)})")
            for path in orphaned:
                if path.is_file():
                    self.stdout.write("   " + str(path))

                    # Uncomment the following to do actual damage
                    # path.unlink()
