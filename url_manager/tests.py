import json
from django.utils import timezone
from django.test import TestCase

from url_manager.models import Url


# Create your tests here.


class UrlManagerModelTest(TestCase):

        def test_url_model_str(self):
            url = Url.objects.create(
                short_endpoint="abc123",
                long_url="https://www.google.com",
                expiration_date="2021-01-01T00:00:00Z",
            )
            self.assertEqual(Url.objects.get(short_endpoint=url.short_endpoint).long_url, "https://www.google.com")



class CreateShortUrlTestCase(TestCase):

    def test_create_short_url_missing_url(self):

        response = self.client.post("/create", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "URL parameter is required")

    def test_create_short_url_invalid_url(self):
        response = self.client.post(
            "/create",
            {"long_url": "google.com"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['error'], "URL parameter is required"
        )

    def test_create_short_url(self):
        response = self.client.post(
            "/create",
            data=json.dumps({"url": "https://www.google.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["short_url"],
                         Url.objects.get(short_endpoint=response.json()["short_url"]).short_endpoint)

class RedirectTestCase(TestCase):

    def setUp(self):
        Url.objects.create(
            short_endpoint="abc123",
            long_url="https://www.google.com"
        )
        Url.objects.create(
            short_endpoint="expire",
            long_url="https://www.google.com",
            expiration_date=timezone.now()
        )

    def test_redirect_to_long_url(self):
        response = self.client.get("/s/abc123", content_type="application/json")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], "https://www.google.com")

    def test_redirect_to_long_url_invalid_short_endpoint(self):
        response = self.client.get("/s/invalid", content_type="application/json",)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "Short URL not found")

    def test_redirect_to_long_url_expired_short_endpoint(self):
        response = self.client.get("/s/expire", content_type="application/json",)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "Short URL has expired")