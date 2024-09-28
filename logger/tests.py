from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import LogEntry


class LogMiddlewareTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.token = RefreshToken.for_user(self.user)

    def test_login_log_entry_creation(self):
        response = self.client.post(
            "/jwt/login/", {"username": "testuser", "password": "password123"}
        )

        log_entry = LogEntry.objects.last()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.path, "/jwt/login/")
        self.assertEqual(log_entry.method, "POST")
        self.assertEqual(log_entry.user, self.user)
        self.assertIn("Status Code: 200", log_entry.message)

    def test_refresh_token_log_entry_creation(self):
        response = self.client.post("/jwt/token/refresh/", {"refresh": str(self.token)})

        log_entry = LogEntry.objects.last()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.path, "/jwt/token/refresh/")
        self.assertEqual(log_entry.method, "POST")
        self.assertEqual(log_entry.user, self.user)
        self.assertIn("Status Code: 200", log_entry.message)

    def test_get_document_log_entry_creation(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get("/document/1/")

        log_entry = LogEntry.objects.last()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.path, "/document/1/")
        self.assertEqual(log_entry.method, "GET")
        self.assertEqual(log_entry.user, self.user)
        self.assertIn("Document ID: 1", log_entry.message)

    def test_invalid_login_log_entry(self):
        response = self.client.post(
            "/jwt/login/", {"username": "invaliduser", "password": "wrongpassword"}
        )

        log_entry = LogEntry.objects.last()
        self.assertIsNotNone(log_entry)

    def test_document_access_without_auth(self):
        response = self.client.get("/document/1/")

        log_entry = LogEntry.objects.last()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.path, "/document/1/")
