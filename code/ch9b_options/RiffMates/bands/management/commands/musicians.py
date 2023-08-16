# RiffMates/bands/management/commands/musicians.py
from datetime import datetime

from bands.models import Musician
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Lists registered musicians"

    def add_arguments(self, parser):
        parser.add_argument(
            "--last_name",
            "-l",
            help=(
                "Query musicians "
                "whose last name is greater than or equal to this value. "
                "Note this is case sensitive."
            ),
        )
        parser.add_argument(
            "--first_name",
            "-f",
            help=(
                "Query musicians "
                "whose first name is greater than or equal to this value. "
                "Note this is case sensitive."
            ),
        )
        parser.add_argument(
            "--birth",
            "-b",
            help=(
                "Query musicians "
                "whose birth date is greater than or equal to this value. "
                "Date must be given in YYYY-MM-DD format."
            ),
        )

    def handle(self, *args, **options):
        musicians = Musician.objects.all()
        if options["last_name"]:
            musicians = musicians.filter(last_name__gte=options["last_name"])

        if options["first_name"]:
            musicians = musicians.filter(first_name__gte=options["first_name"])

        if options["birth"]:
            try:
                birth = datetime.strptime(options["birth"], "%Y-%m-%d")
            except ValueError:
                raise CommandError(
                    "Birth date must be provided in YYYY-MM-DD format"
                )

            musicians = musicians.filter(birth__gte=birth)

        for musician in musicians:
            self.stdout.write(
                f"{musician.last_name}, {musician.first_name} "
                f"({musician.birth})"
            )
