# home/tests.py
from django.test import TestCase


class TestHome(TestCase):
    def test_credits(self):
        response = self.client.get("/credits/")
        self.assertEqual(200, response.status_code)
