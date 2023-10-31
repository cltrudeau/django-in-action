# RiffMates/bands/tests.py
import io
import tempfile
from base64 import b64decode
from datetime import date

from bands.models import Musician, Venue
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings


def raises_an_error():
    raise ValueError()


class TestBands(TestCase):
    def setUp(self):
        self.musician = Musician.objects.create(
            first_name="First", last_name="Last", birth=date(1900, 1, 1)
        )

        self.PASSWORD = "notsecure"
        self.owner = User.objects.create_user("owner", password=self.PASSWORD)
        self.member = User.objects.create_user("member", password=self.PASSWORD)
        self.admin = User.objects.create_superuser(
            "admin", password=self.PASSWORD
        )

        # Base64 encoded version of a single pixel GIF image
        image = "R0lGODdhAQABAIABAP///wAAACwAAAAAAQABAAACAkQBADs="
        self.image = b64decode(image)

    def test_musician_view(self):
        url = f"/bands/musician/{self.musician.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.context["musician"].id, self.musician.id)
        self.assertIn(self.musician.first_name, str(response.content))

    def test_musician_404(self):
        url = "/bands/musician/10/"
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_raises_an_error(self):
        with self.assertRaises(ValueError):
            raises_an_error()

    def test_edit_venue(self):
        self.client.login(username="owner", password=self.PASSWORD)

        # Verify the page fetch works
        url = "/bands/edit_venue/0/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

        # Create a new Venue
        data = {
            "name": "Name",
            "description": "Description",
        }
        response = self.client.post(url, data)

        self.assertEqual(302, response.status_code)

        # Validate the Venue was created
        venue = Venue.objects.first()
        self.assertEqual(data["name"], venue.name)
        self.assertEqual(data["description"], venue.description)
        self.assertTrue(
            self.owner.userprofile.venues_controlled.filter(
                id=venue.id
            ).exists()
        )

        # Now edit that Venue
        url = f"/bands/edit_venue/{venue.id}/"
        data["name"] = "Edited Name"
        response = self.client.post(url, data)

        self.assertEqual(302, response.status_code)
        venue = Venue.objects.first()
        self.assertEqual(data["name"], venue.name)

        # Verify that a non-owner can't edit
        self.client.login(username="member", password=self.PASSWORD)
        response = self.client.post(url, data)
        self.assertEqual(404, response.status_code)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_edit_venue_picture(self):
        file = SimpleUploadedFile("test.gif", self.image)
        data = {
            "name": "Name",
            "description": "Description",
            "picture": file,
        }

        self.client.login(username="owner", password=self.PASSWORD)
        url = "/bands/edit_venue/0/"
        response = self.client.post(url, data)

        self.assertEqual(302, response.status_code)
        venue = Venue.objects.first()
        self.assertIsNotNone(venue.picture)

    def test_edit_musician(self):
        self.client.login(username="owner", password=self.PASSWORD)

        # Verify the page fetch works
        url = "/bands/edit_musician/0/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

        # Create a new Musician (NB: one already exists from .setup())
        file = SimpleUploadedFile("test.gif", self.image)
        data = {
            "first_name": "First2",
            "last_name": "Last2",
            "birth": date(1900, 1, 2),
            "description": "Description2",
            "picture": file,
        }
        response = self.client.post(url, data)

        self.assertEqual(302, response.status_code)

        # Validate the Musician was created
        musician = Musician.objects.last()
        self.assertEqual(data["first_name"], musician.first_name)
        self.assertEqual(data["last_name"], musician.last_name)
        self.assertEqual(data["description"], musician.description)
        self.assertEqual(data["birth"], musician.birth)
        self.assertIsNotNone(musician.picture)
        self.assertTrue(
            self.owner.userprofile.musician_profiles.filter(
                id=musician.id
            ).exists()
        )

        # Now edit the Musician (recreate the file to reset its stream)
        url = f"/bands/edit_musician/{musician.id}/"
        data["first_name"] = "Edited Name"
        file = SimpleUploadedFile("test.gif", self.image)
        data["picture"] = file
        response = self.client.post(url, data)

        self.assertEqual(302, response.status_code)
        musician = Musician.objects.last()
        self.assertEqual(data["first_name"], musician.first_name)

        # Verify that a superuser can edit
        self.client.login(username="admin", password=self.PASSWORD)
        file = SimpleUploadedFile("test.gif", self.image)
        data["picture"] = file
        data["first_name"] = "Super Edited Name"
        response = self.client.post(url, data)

        self.assertEqual(302, response.status_code)
        musician = Musician.objects.last()
        self.assertEqual(data["first_name"], musician.first_name)

        # Verify that a non-owner can't edit
        self.client.login(username="member", password=self.PASSWORD)
        response = self.client.post(url, data)
        self.assertEqual(404, response.status_code)

    def test_musicians(self):
        # Create 9 more Musicians (one exists from .setUp())
        for x in range(2, 11):
            Musician.objects.create(
                first_name=f"First{x}",
                last_name=f"Last{x}",
                birth=date(1900, 1, x),
            )

        # Test URL with no arguments, 10 musicians means no pagination
        url = "/bands/musicians/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(10, len(response.context["musicians"]))
        self.assertFalse(response.context["page"].has_previous())
        self.assertFalse(response.context["page"].has_next())

        # Test with 5 per page
        url = "/bands/musicians/?items_per_page=5"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.context["musicians"]))
        self.assertFalse(response.context["page"].has_previous())
        self.assertTrue(response.context["page"].has_next())

        # Test with 5 per page, page #2
        url = "/bands/musicians/?items_per_page=5&page=2"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.context["musicians"]))
        self.assertTrue(response.context["page"].has_previous())
        self.assertFalse(response.context["page"].has_next())

        # Test bad page size
        url = "/bands/musicians/?items_per_page=-1"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(10, len(response.context["musicians"]))
        self.assertFalse(response.context["page"].has_other_pages())


class TestMusiciansCommand(TestCase):
    def setUp(self):
        self.musician = Musician.objects.create(
            first_name="First", last_name="Last", birth=date(1900, 1, 1)
        )

    def test_command(self):
        output = io.StringIO()

        call_command("musicians", stdout=output)
        self.assertIn("First", output.getvalue())
