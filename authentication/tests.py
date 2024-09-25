from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTokenTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_login_success(self):
        response = self.client.post(
            "/jwt/login/", {"username": "testuser", "password": "testpass"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failure(self):
        response = self.client.post(
            "/jwt/login/", {"username": "testuser", "password": "wrongpassword"}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh_success(self):
        response_obtain = self.client.post(
            "/jwt/login/", {"username": "testuser", "password": "testpass"}
        )
        access_token = response_obtain.data["refresh"]
        response_refresh = self.client.post(
            "/jwt/token/refresh/", {"refresh": access_token}
        )

        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        self.assertIn("access", response_refresh.data)
        self.assertIn("refresh", response_refresh.data)

    def test_token_refresh_failure(self):
        response_refresh = self.client.post(
            "/jwt/token/refresh/", {"refresh": "invalid_refresh_token"}
        )

        self.assertEqual(response_refresh.status_code, status.HTTP_401_UNAUTHORIZED)
