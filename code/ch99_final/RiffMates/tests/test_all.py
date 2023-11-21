# RiffMates/tests/test_all.py
import io
import json
from datetime import date
from unittest.mock import patch
from urllib.parse import quote_plus

from bands.models import Band, Musician, Room, Venue
from content.models import MusicianBandChoice, SeekingAd
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from promoters.models import Promoter


class CoreTests(TestCase):
    def setUp(self):
        self.musician = Musician.objects.create(
            first_name="First",
            last_name="Last",
            birth=date(1900, 1, 1),
            description="description",
        )

        self.PASSWORD = "notsecure"
        self.owner = User.objects.create_user("owner", password=self.PASSWORD)
        self.member = User.objects.create_user("member", password=self.PASSWORD)
        self.admin = User.objects.create_superuser(
            "admin", password=self.PASSWORD
        )

    def check_home_app(self):
        # Credits page
        response = self.client.get("/credits/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Nicky", str(response.content))

        # About page
        response = self.client.get("/about/")
        self.assertEqual(200, response.status_code)
        self.assertIn("RiffMates About", str(response.content))

        # Version page
        response = self.client.get("/version/")
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertIn("version", data)

        # News: skipping this test as it has two "extends" tags in it due to
        # how the juli content works, just not worth dealing with

        # Advanced News
        response = self.client.get("/adv_news/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Advanced News", str(response.content))

    def test_home(self):
        # Check common unauthenticated
        self.check_home_app()

        # Check home page and base header isn't there
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Welcome to RiffMates", str(response.content))
        self.assertNotIn("Hello, owner", str(response.content))

        # Check same pages, authenticated
        self.client.login(username="owner", password=self.PASSWORD)
        self.check_home_app()

        # Check home page and base header is there
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Welcome to RiffMates", str(response.content))
        self.assertIn("Hello, owner", str(response.content))

    def test_bands(self):
        # Tests for bands app not covered by its own unit tests (from the
        # book)

        # Musician view as admin
        self.client.login(username="admin", password=self.PASSWORD)
        response = self.client.get(f"/bands/musician/{self.musician.id}/")
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context["musician"].controller)

        # Musician view as an associated profile
        self.owner.userprofile.musician_profiles.add(self.musician)
        self.client.login(username="owner", password=self.PASSWORD)
        response = self.client.get(f"/bands/musician/{self.musician.id}/")
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context["musician"].controller)

        # Edit musician view doing a GET on a specific musician ID (using
        # owner/controller created in previous lines)
        response = self.client.get(f"/bands/edit_musician/{self.musician.id}/")
        self.assertEqual(200, response.status_code)

        # Max pagination works
        for n in range(1, 60):
            Musician.objects.create(
                first_name=f"first{n}",
                last_name=f"last{n}",
                birth=date(1900, 1, 25),
            )

        response = self.client.get("/bands/musicians/?items_per_page=55")
        self.assertEqual(200, response.status_code)
        self.assertEqual(50, len(response.context["musicians"]))

        # Weird page number requests work
        response = self.client.get("/bands/musicians/?page=0")
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context["page"].number)

        response = self.client.get("/bands/musicians/?page=1000")
        self.assertEqual(200, response.status_code)
        self.assertEqual(6, response.context["page"].number)

        # Band view
        band = Band.objects.create(name="band")
        response = self.client.get(f"/bands/band/{band.id}/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Band Details", str(response.content))

        # Bands view
        response = self.client.get("/bands/bands/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Band Listing", str(response.content))

        # Venue view, anonymous user
        venue = Venue.objects.create(name="venue")
        self.client.logout()
        response = self.client.get("/bands/venues/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Venue Listing", str(response.content))
        self.assertFalse(response.context["venues"][0].controlled)

        # Venue view, owner
        self.owner.userprofile.venues_controlled.add(venue)
        self.client.login(username="owner", password=self.PASSWORD)
        response = self.client.get("/bands/venues/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Venue Listing", str(response.content))
        self.assertTrue(response.context["venues"][0].controlled)

        # Restricted page view
        self.client.logout()
        response = self.client.get("/bands/restricted_page/")
        self.assertEqual(302, response.status_code)
        self.client.login(username="owner", password=self.PASSWORD)
        response = self.client.get("/bands/restricted_page/")
        self.assertEqual(200, response.status_code)

        # Musician restricted view, as non-owner (anonymous triggers login
        # page)
        mid = self.musician.id
        self.client.logout()
        self.client.login(username="member", password=self.PASSWORD)
        response = self.client.get(f"/bands/musician_restricted/{mid}/")
        self.assertEqual(404, response.status_code)

        # Musician restricted view, as profile associated with musician
        self.client.login(username="owner", password=self.PASSWORD)
        response = self.client.get(f"/bands/musician_restricted/{mid}/")
        self.assertEqual(200, response.status_code)

        # Musician restricted view, owner's band mate
        band = Band.objects.create(name="pair")
        m2 = Musician.objects.create(
            first_name="f2",
            last_name="l2",
            birth=date(1900, 1, 25),
            description="description",
        )
        band.musicians.add(self.musician)
        band.musicians.add(m2)

        response = self.client.get(f"/bands/musician_restricted/{m2.id}/")
        self.assertEqual(200, response.status_code)

        # Venues restricted view, owner already controls a venue from earlier
        # test
        response = self.client.get("/bands/venues_restricted/")
        self.assertEqual(200, response.status_code)

        # Venues restricted, anonymous
        self.client.logout()
        response = self.client.get("/bands/venues_restricted/")
        self.assertEqual(302, response.status_code)

        # Edit venue view, GET scenario with a venue
        self.client.login(username="owner", password=self.PASSWORD)
        response = self.client.get(f"/bands/edit_venue/{venue.id}/")
        self.assertEqual(200, response.status_code)

    def test_content(self):
        # Comment view GET
        response = self.client.get("/content/comment/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Comment", str(response.content))

        # Comment view POST
        data = {
            "name": "Name",
            "comment": "Comment",
        }
        response = self.client.post("/content/comment/", data)
        self.assertEqual(302, response.status_code)

        # Comment accepted view
        response = self.client.get("/content/comment_accepted/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Comment Accepted", str(response.content))

        # List ads
        response = self.client.get("/content/list_ads/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Musicians Seeking", str(response.content))

        # ---
        # Seeking Ad view, GET
        self.client.login(username="owner", password=self.PASSWORD)
        response = self.client.get("/content/seeking_ad/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Seeking Ad", str(response.content))

        # Seeking Ad view, POST
        band = Band.objects.create(name="band")
        data = {
            "seeking": MusicianBandChoice.MUSICIAN,
            "band": band.id,
            "content": "content",
        }
        response = self.client.post("/content/seeking_ad/", data)
        self.assertEqual(302, response.status_code)

        ad = SeekingAd.objects.first()

        # Edit Seeking Ad, GET as owner
        response = self.client.get(f"/content/edit_seeking_ad/{ad.id}/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Seeking Ad", str(response.content))

        # Edit Seeking Ad, GET as admin
        self.client.login(username="admin", password=self.PASSWORD)
        response = self.client.get(f"/content/edit_seeking_ad/{ad.id}/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Seeking Ad", str(response.content))

        # Edit Seeking Ad, GET as non-owner (rejected)
        self.client.login(username="member", password=self.PASSWORD)
        response = self.client.get(f"/content/edit_seeking_ad/{ad.id}/")
        self.assertEqual(404, response.status_code)

        # Edit Seeking Ad, POST as owner
        self.client.login(username="owner", password=self.PASSWORD)
        data["content"] = "owner edit content"
        response = self.client.post(f"/content/edit_seeking_ad/{ad.id}/", data)
        self.assertEqual(302, response.status_code)

        # Edit Seeking Ad, POST as admin
        self.client.login(username="admin", password=self.PASSWORD)
        data["content"] = "admin edit content"
        response = self.client.post(f"/content/edit_seeking_ad/{ad.id}/", data)
        self.assertEqual(302, response.status_code)

        # Edit Seeking Ad, POST as member (rejected)
        self.client.login(username="member", password=self.PASSWORD)
        response = self.client.post(f"/content/edit_seeking_ad/{ad.id}/", data)
        self.assertEqual(404, response.status_code)

    def test_musicians_command(self):
        Musician.objects.create(
            first_name="A-name",
            last_name="D-name",
            birth=date(1900, 1, 15),
            description="description",
        )
        Musician.objects.create(
            first_name="B-name",
            last_name="E-name",
            birth=date(1900, 2, 15),
            description="description",
        )
        Musician.objects.create(
            first_name="C-name",
            last_name="F-name",
            birth=date(1900, 3, 15),
            description="description",
        )

        # No args
        output = io.StringIO()
        call_command("musicians", stdout=output)
        self.assertIn("A-name", output.getvalue())

        # First name filter
        output = io.StringIO()
        call_command("musicians", first_name="B", stdout=output)
        self.assertNotIn("A-name", output.getvalue())
        self.assertIn("B-name", output.getvalue())
        self.assertIn("C-name", output.getvalue())

        # Last name filter
        output = io.StringIO()
        call_command("musicians", last_name="E", stdout=output)
        self.assertNotIn("D-name", output.getvalue())
        self.assertIn("E-name", output.getvalue())
        self.assertIn("F-name", output.getvalue())

        # Date filter
        output = io.StringIO()
        call_command("musicians", birth="1900-02-01", stdout=output)
        self.assertNotIn("A-name", output.getvalue())
        self.assertIn("B-name", output.getvalue())
        self.assertIn("C-name", output.getvalue())

        # Bad date filter
        with self.assertRaises(CommandError) as error:
            call_command("musicians", birth="Christmas", stdout=output)

        self.assertIn("Birth date must", str(error.exception))

    def test_venues_command(self):
        venue = Venue.objects.create(name="venue")
        Room.objects.create(name="room", venue=venue)

        # No args
        output = io.StringIO()
        call_command("venues", stdout=output)
        self.assertIn("venue", output.getvalue())
        self.assertNotIn("room", output.getvalue())

        # Room flag
        output = io.StringIO()
        call_command("venues", rooms=True, stdout=output)
        self.assertIn("venue", output.getvalue())
        self.assertIn("room", output.getvalue())

    def test_api(self):
        # Home
        response = self.client.get("/api/v1/home/")
        self.assertEqual(200, response.status_code)
        self.assertIn("RiffMates rocks", str(response.content))

        # Version
        response = self.client.get("/api/v1/home/version/")
        self.assertEqual(200, response.status_code)
        result = json.loads(response.content)
        self.assertEqual("0.0.1", result["version"])

        # Promoter
        promoter = Promoter.objects.create(
            common_name="fn", full_name="fn ln", famous_for="stuff"
        )

        response = self.client.get("/api/v1/promoters/promoters/")
        self.assertEqual(200, response.status_code)
        result = json.loads(response.content)
        self.assertEqual(1, len(result))
        self.assertEqual("fn ln", result[0]["full_name"])

        response = self.client.get(f"/api/v1/promoters/promoter/{promoter.id}/")
        self.assertEqual(200, response.status_code)
        result = json.loads(response.content)
        self.assertEqual("fn ln", result["full_name"])

        # Venues
        headers = {
            "X-API-KEY": settings.NINJA_API_KEY,
        }

        data = {
            "name": "v-name",
            "description": "v-description",
        }
        response = self.client.post(
            "/api/v1/bands/venue/", data, "application/json", headers=headers
        )
        self.assertEqual(200, response.status_code)

        venue = Venue.objects.first()
        self.assertEqual("v-name", venue.name)

        response = self.client.get("/api/v1/bands/venues/")
        self.assertEqual(200, response.status_code)
        result = json.loads(response.content)
        self.assertEqual(1, len(result))
        self.assertEqual("v-name", result[0]["name"])

        response = self.client.get(f"/api/v1/bands/venue/{venue.id}/")
        self.assertEqual(200, response.status_code)
        result = json.loads(response.content)
        self.assertEqual("v-name", result["name"])

        data["name"] = "v-name edit"
        response = self.client.put(
            f"/api/v1/bands/venue/{venue.id}/",
            data,
            "application/json",
            headers=headers,
        )
        self.assertEqual(200, response.status_code)
        venue = Venue.objects.first()
        self.assertEqual("v-name edit", venue.name)

        response = self.client.delete(
            f"/api/v1/bands/venue/{venue.id}/", headers=headers
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, Venue.objects.all().count())

        # Bands
        band = Band.objects.create(name="b-name")
        band.musicians.add(self.musician)

        response = self.client.get("/api/v1/bands/bands/")
        self.assertEqual(200, response.status_code)
        result = json.loads(response.content)
        self.assertEqual(1, len(result))
        self.assertEqual("b-name", result[0]["name"])
        self.assertEqual("First", result[0]["musicians"][0]["first_name"])

        # Musician
        data = {
            "first_name": "first edit",
            "last_name": "last edit",
            "birth": date(1800, 8, 30),
            "description": "desc edit",
        }

        response = self.client.put(
            f"/api/v1/bands/musician/{self.musician.id}/",
            data,
            "application/json",
            headers=headers,
        )
        self.assertEqual(200, response.status_code)
        m = Musician.objects.get(id=self.musician.id)
        self.assertEqual("first edit", m.first_name)

    @patch("time.sleep", return_value=None)
    def test_htmx(self, patched_sleep):
        # Simple load views, just make sure they run
        response = self.client.get("/promoters/promoters/")
        self.assertEqual(200, response.status_code)

        response = self.client.get("/promoters/partial_promoters/")
        self.assertEqual(200, response.status_code)

        # HTMX header
        headers = {
            "HX-Request": "true",
        }

        # Search musicians
        data = (
            ("AF1", "BL1"),
            ("AF2", "BL2"),
            ("AF3", "BL3"),
            ("CF1", "DL1"),
            ("CF2", "DL2"),
            ("CF3", "DL3"),
        )

        for first_name, last_name in data:
            Musician.objects.create(
                first_name=first_name,
                last_name=last_name,
                birth=date(1900, 1, 31),
            )

        url = (
            "/bands/search_musicians/?search_text="
            + quote_plus("A D")
            + "&items_per_page=4"
        )
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        result = response.context
        self.assertEqual(4, len(result["musicians"]))
        self.assertEqual(True, result["has_more"])
        self.assertEqual(2, result["next_page"])
        self.assertIn("templates/search_musicians", str(response.content))

        # Do it again in HTMX mode
        url = (
            "/bands/search_musicians/?search_text="
            + quote_plus("A D")
            + "&items_per_page=4&page=2"
        )
        response = self.client.get(url, headers=headers)

        self.assertEqual(200, response.status_code)
        result = response.context
        self.assertEqual(2, len(result["musicians"]))
        self.assertEqual(False, result["has_more"])
        self.assertEqual(3, result["next_page"])
        self.assertIn(
            "templates/partials/musician_results", str(response.content)
        )

        # Room editor
        venue = Venue.objects.create(name="venue")
        room = Room.objects.create(name="room", venue=venue)
        self.owner.userprofile.venues_controlled.add(venue)

        self.client.login(username="owner", password=self.PASSWORD)

        response = self.client.get(f"/bands/room_editor/{venue.id}/")
        self.assertEqual(200, response.status_code)

        response = self.client.get(f"/bands/edit_room_form/{room.id}/")
        self.assertEqual(200, response.status_code)
        self.assertIn(
            "templates/partials/edit_room_form", str(response.content)
        )

        data = {
            "name": "edited room",
        }
        response = self.client.post(f"/bands/edit_room_form/{room.id}/", data)
        self.assertEqual(200, response.status_code)
        self.assertIn("templates/partials/show_room", str(response.content))

        room = Room.objects.get(id=room.id)
        self.assertEqual("edited room", room.name)

        response = self.client.get(f"/bands/show_room_partial/{room.id}/")
        self.assertEqual(200, response.status_code)
        self.assertIn("templates/partials/show_room", str(response.content))

        # Tabbed interface
        response = self.client.get("/bands/tabbed_listing/")
        self.assertEqual(200, response.status_code)

        # Ad search
        band = Band.objects.create(name="band")
        SeekingAd.objects.create(
            seeking=MusicianBandChoice.MUSICIAN,
            band=band,
            content="one two",
            owner=self.owner,
        )
        SeekingAd.objects.create(
            seeking=MusicianBandChoice.MUSICIAN,
            band=band,
            content="two three",
            owner=self.owner,
        )
        SeekingAd.objects.create(
            seeking=MusicianBandChoice.MUSICIAN,
            band=band,
            content="four",
            owner=self.owner,
        )

        url = (
            "/content/search_ads/?search_text="
            + quote_plus("one three")
            + "&items_per_page=1"
        )
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        result = response.context
        self.assertEqual(1, len(result["ads"]))
        self.assertEqual(True, result["has_more"])
        self.assertEqual(2, result["next_page"])
        self.assertIn("templates/search_ads", str(response.content))

        # Do it again in HTMX mode
        url = (
            "/content/search_ads/?search_text="
            + quote_plus("one three")
            + "&items_per_page=1&page=2"
        )
        response = self.client.get(url, headers=headers)

        self.assertEqual(200, response.status_code)
        result = response.context
        self.assertEqual(1, len(result["ads"]))
        self.assertEqual(False, result["has_more"])
        self.assertEqual(3, result["next_page"])
        self.assertIn("templates/partials/ad_results", str(response.content))
